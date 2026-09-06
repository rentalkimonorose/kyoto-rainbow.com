use lib "librarys/SMTPS/lib";
use Net::SMTP;
use Net::SMTP::TLS;

sub _SENDMAIL {
	my($to,$from,$name,$subject,$body,$attached,$htmlmail) = @_;
	my($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	@month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	$smtpdate = sprintf("%s, %d %s %04d %02d:%02d:%02d +0900 (JST)",$week[$wday],$mday,$month[$mon],$year+1900,$hour,$min,$sec);
	
	$SMTP = Net::SMTP::TLS->new(
		$config{'SMTPserver'},
		Port => $config{'SMTPport'},
		User => $config{'SMTPuser'},
		Password	 => $config{'SMTPpasswd'}
	) || die "Connect failed over tls";
	
	$SMTP->mail($from);
	$SMTP->to($to);
	$SMTP->data();
	$SMTP->datasend("Date: ${smtpdate}\n");
	$SMTP->datasend(&_MAILHEADER($to,$from,$name,$subject,$body,$attached,$htmlmail));
	$SMTP->dataend();
	$SMTP->quit;
}
1;