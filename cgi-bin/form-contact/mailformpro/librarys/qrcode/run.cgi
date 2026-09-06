if($_TEXT{'qrcode.responder'}){
	push @ResAttachedFiles,&_ATTACHEDIMAGE("qrcode.png",&_QRCODE_GET($_TEXT{'qrcode.responder'}));
}
if($_TEXT{'qrcode.mail'}){
	push @AttachedFiles,&_ATTACHEDIMAGE("qrcode.png",&_QRCODE_GET($_TEXT{'qrcode.mail'}));
}
1;