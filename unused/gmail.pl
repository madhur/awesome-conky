#!/usr/bin/perl
use strict;
use warnings;
use Mail::IMAPClient;
use IO::Socket::SSL;

my $socket = IO::Socket::SSL->new(
   PeerAddr => 'imap.gmail.com',
   PeerPort => 993,
  )
  or die "socket(): $@";

my $client = Mail::IMAPClient->new(
   Socket   => $socket,
   User     => 'username',
   Password => 'password',
  )
  or die "new(): $@";

my $cont = 1;
$client->select('INBOX');
my @mails = ($client->seen(),$client->unseen);
foreach my $id (@mails) {
    my $from = $client->get_header($id, 'From');
    if ($from =~ /([a-zA-Z\_\-\.0-9]+@[a-zA-Z\_\-0-9]+\.[0-9a-zA-Z\.\-\_]+)/) {
        my $email = lc $1;
        print "email[$email]\n";
    };
};

$client->logout();