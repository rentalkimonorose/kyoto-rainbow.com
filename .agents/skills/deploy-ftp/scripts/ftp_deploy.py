#!/usr/bin/env python3
import os
import sys
import json
import argparse
import subprocess
import tempfile
from ftplib import FTP, FTP_TLS

def run_git(args, cwd=None):
    """Run a git command and return its stdout as a string."""
    try:
        res = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: git {' '.join(args)}")
        print(f"Error output: {e.stderr.strip()}")
        sys.exit(1)

def ensure_remote_dir(ftp, remote_dir):
    """Recursively ensure that a remote directory exists relative to current dir."""
    if not remote_dir or remote_dir == '.':
        return
    
    parts = [p for p in remote_dir.replace('\\', '/').split('/') if p]
    original_cwd = ftp.pwd()
    
    for part in parts:
        try:
            ftp.cwd(part)
        except Exception:
            try:
                print(f"Creating remote directory: {ftp.pwd()}/{part}")
                ftp.mkd(part)
                ftp.cwd(part)
            except Exception as e:
                print(f"Failed to create remote directory '{part}' under '{ftp.pwd()}': {e}")
                ftp.cwd(original_cwd)
                raise
                
    ftp.cwd(original_cwd)

def upload_file(ftp, local_path, remote_path):
    """Upload a single file to the FTP server."""
    remote_dir = os.path.dirname(remote_path)
    if remote_dir:
        ensure_remote_dir(ftp, remote_dir)
        
    filename = os.path.basename(remote_path)
    # FTP expects forward slashes for remote directory navigation
    remote_dir_normalized = remote_dir.replace('\\', '/')
    
    original_cwd = ftp.pwd()
    if remote_dir_normalized and remote_dir_normalized != '.':
        ftp.cwd(remote_dir_normalized)
        
    try:
        print(f"Uploading: {local_path} -> {remote_path}")
        with open(local_path, 'rb') as f:
            ftp.storbinary(f"STOR {filename}", f)
    finally:
        ftp.cwd(original_cwd)

def delete_file(ftp, remote_path):
    """Delete a file from the FTP server."""
    try:
        print(f"Deleting remote file: {remote_path}")
        ftp.delete(remote_path.replace('\\', '/'))
    except Exception as e:
        print(f"Warning: Could not delete remote file {remote_path} (it may not exist): {e}")

def main():
    parser = argparse.ArgumentParser(description="Git-based FTP deployment helper")
    parser.add_argument('--config', default='.ftp_config.json', help='Path to FTP configuration file')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without modifying files')
    parser.add_argument('--force-full', action='store_true', help='Force a full deployment of all tracked files')
    parser.add_argument('--catchup', action='store_true', help='Update remote deployment marker to current commit without uploading files')
    parser.add_argument('--repo-path', default='.', help='Path containing the Git repository')
    args = parser.parse_args()

    # Find the repository path
    repo_absolute_path = os.path.abspath(args.repo_path)
    if not os.path.isdir(repo_absolute_path):
        print(f"Error: Repository directory not found at {repo_absolute_path}")
        sys.exit(1)

    # Resolve config file path relative to repo or absolute
    config_path = args.config
    if not os.path.isabs(config_path):
        config_path = os.path.join(repo_absolute_path, config_path)

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        print("Please copy .ftp_config.json.template to .ftp_config.json and populate it with details.")
        sys.exit(1)

    # Load configuration
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        sys.exit(1)

    host = config.get('host')
    username = config.get('username')
    password = config.get('password')
    port = config.get('port', 21)
    remote_path = config.get('remote_path', '/')
    use_tls = config.get('use_tls', False)

    if not host or not username or not password:
        print("Error: Missing required configuration keys (host, username, password)")
        sys.exit(1)

    # Get current git HEAD commit
    current_commit = run_git(['rev-parse', 'HEAD'], cwd=repo_absolute_path)
    print(f"Current repository commit (HEAD): {current_commit}")

    # Connect to FTP
    print(f"Connecting to FTP server {host}:{port}...")
    if use_tls:
        ftp = FTP_TLS()
    else:
        ftp = FTP()
        
    try:
        ftp.connect(host, port)
        ftp.login(username, password)
        if use_tls:
            ftp.prot_p() # Secure the data connection
        print("Connected and authenticated successfully.")
        
        # Navigate to target directory
        if remote_path and remote_path != '/':
            print(f"Navigating to remote directory: {remote_path}")
            # Try to navigate, if fails, create it
            try:
                ftp.cwd(remote_path)
            except Exception:
                ensure_remote_dir(ftp, remote_path)
                ftp.cwd(remote_path)
    except Exception as e:
        print(f"Failed to connect or log in to FTP server: {e}")
        sys.exit(1)

    # Determine last deployed commit
    commit_file = '.git-ftp-commit'

    if args.catchup:
        if args.dry_run:
            print(f"[Dry Run] Would update remote deployment marker to current commit: {current_commit}")
            ftp.quit()
            return
        
        print(f"Updating remote deployment marker to current commit: {current_commit} (Catchup mode, no files uploaded)...")
        success = True
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tf:
                tf.write(current_commit)
                tf.flush()
                temp_name = tf.name
            try:
                with open(temp_name, 'rb') as f:
                    ftp.storbinary(f"STOR {commit_file}", f)
            finally:
                os.unlink(temp_name)
            print("Catchup completed successfully!")
        except Exception as e:
            print(f"Failed to update remote deployment marker: {e}")
            success = False
        finally:
            ftp.quit()
        if not success:
            sys.exit(1)
        return

    last_commit = None
    
    if not args.force_full:
        try:
            # Try to read last commit from server
            print(f"Checking for remote tracking file '{commit_file}'...")
            commit_lines = []
            ftp.retrlines(f"RETR {commit_file}", commit_lines.append)
            if commit_lines:
                last_commit = commit_lines[0].strip()
                print(f"Found remote deployment marker. Last deployed commit: {last_commit}")
        except Exception:
            print("No remote deployment marker found. Defaulting to full deployment.")

    # Calculate what changes to deploy
    files_to_upload = []
    files_to_delete = []
    
    is_full_deploy = True
    if last_commit and not args.force_full:
        # Check if the last commit exists in local repository history
        try:
            run_git(['cat-file', '-e', last_commit], cwd=repo_absolute_path)
            is_full_deploy = False
        except Exception:
            print(f"Warning: Last deployed commit {last_commit} is not in local history. Performing full deployment.")

    if is_full_deploy:
        print("Preparing FULL deployment of all git-tracked files...")
        # Get all git tracked files
        tracked_files_str = run_git(['ls-files'], cwd=repo_absolute_path)
        files_to_upload = [f.strip() for f in tracked_files_str.split('\n') if f.strip()]
    else:
        print(f"Calculating difference between {last_commit} and HEAD...")
        diff_str = run_git(['diff', '--name-status', last_commit, 'HEAD'], cwd=repo_absolute_path)
        for line in diff_str.split('\n'):
            if not line.strip():
                continue
            parts = line.split('\t')
            status = parts[0]
            if status.startswith('R'): # Renamed
                old_file = parts[1]
                new_file = parts[2]
                files_to_delete.append(old_file)
                files_to_upload.append(new_file)
            elif status == 'D': # Deleted
                files_to_delete.append(parts[1])
            else: # Added, Modified, type changed, etc.
                files_to_upload.append(parts[1])

    # Print summary of actions
    print("\n--- Deployment Summary ---")
    print(f"Files to upload: {len(files_to_upload)}")
    for f in files_to_upload[:15]:
        print(f"  + {f}")
    if len(files_to_upload) > 15:
        print(f"  ... and {len(files_to_upload) - 15} more")
        
    print(f"Files to delete: {len(files_to_delete)}")
    for f in files_to_delete[:15]:
        print(f"  - {f}")
    if len(files_to_delete) > 15:
        print(f"  ... and {len(files_to_delete) - 15} more")
    print("--------------------------\n")

    if args.dry_run:
        print("Dry run requested. No changes made.")
        ftp.quit()
        return

    # Execute changes
    success = True
    try:
        # Delete remote files first
        for rel_path in files_to_delete:
            delete_file(ftp, rel_path)
            
        # Upload new/modified files
        for rel_path in files_to_upload:
            local_file_path = os.path.join(repo_absolute_path, rel_path)
            if os.path.exists(local_file_path):
                upload_file(ftp, local_file_path, rel_path)
            else:
                print(f"Warning: Local file not found: {local_file_path}")

        # Update remote commit hash file
        print(f"Updating remote deployment marker with commit: {current_commit}")
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tf:
            tf.write(current_commit)
            tf.flush()
            temp_name = tf.name
            
        try:
            with open(temp_name, 'rb') as f:
                ftp.storbinary(f"STOR {commit_file}", f)
        finally:
            os.unlink(temp_name)
            
        print("\nDeployment completed successfully!")
        
    except Exception as e:
        print(f"An error occurred during file transfer: {e}")
        success = False
    finally:
        try:
            ftp.quit()
        except Exception:
            pass

    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
