open INP, "<signatures_test.txt";
my %cluster = ();
while(<INP>){
	chomp;
	my @input = split /\t/, $_;
	push @{$cluster{$input[-1]}}, $input[0];

}
close INP;

open OUT, ">clusters_test.txt";

my $cid = 0;
for my $key (sort keys %cluster){
	my $instance_list = join "|", @{$cluster{$key}};
	$cid++;
	print OUT "$cid\t$instance_list\n";

}
close OUT;

open INP, "<signatures_train.txt";
my %cluster = ();
while(<INP>){
	chomp;
	my @input = split /\t/, $_;
	push @{$cluster{$input[-1]}}, $input[0];

}
close INP;

open OUT, ">clusters_train.txt";

my $cid = 0;
for my $key (sort keys %cluster){
	my $instance_list = join "|", @{$cluster{$key}};
	$cid++;
	print OUT "$cid\t$instance_list\n";

}
close OUT;
