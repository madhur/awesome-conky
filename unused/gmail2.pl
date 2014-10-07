#!/usr/bin/perl

# Put this in ~/.gmail/ and use "crontab -e" to add something like
# "* * * * * ~/.gmail/gmail.pl > /dev/null" to run it every minute.
# ${exec cat ~/.gmail/.gmail_top} shows your inbox in Conky.
# Note that this was intended to be used with Gmail or any other
# ssl-enabled pop3 server.

# beginning of configuration

# pop3 host
$pop_host = "pop.gmail.com";

# pop3 username (for Gmail, I didn't have to put @gmail.com at the end)
$pop_user = "user";

# pop3 password
$pop_pass = "Password";

# ssl port number (995 is what Gmail uses)
$ssl_port = "995";

# ssl protocol
$ssl_prot = "tcp";

# number of emails to show
$dis_numb = "6";

# end of configuration

use Mail::POP3Client;
use IO::Socket::SSL;

  my $socket = IO::Socket::SSL->new( PeerAddr => $pop_host,
                                     PeerPort => $ssl_port,
                                     Proto    => $ssl_prot);
  my $pop = Mail::POP3Client->new();
  $pop->User($pop_user);
  $pop->Pass($pop_pass);
  $pop->Socket($socket);
  $pop->Connect();

$msg_count = $pop->Count();

for ($i = $msg_count, $j = 0; $i >= $msg_count-($dis_numb-1); $i--, $j++) {
  foreach ( $pop->Head( $i ) ) {
    #/^(From|Subject):\s+/i and print $_, "\n";
    if ($_ =~ m/^From:/) {
      ($from) = ($_ =~ m#^From: .*<(.*)>#);
      $from = substr($from, 0, 30);
      $out .= "$j = $from\n";
    }
  }
  #chop $out;
  `echo -e "$out"> ~/.gmail/.gmail_top`;
}

$pop->Close();
