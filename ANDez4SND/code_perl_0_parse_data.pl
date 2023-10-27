open INP,"<sample_prism_500_kl - sample_prism_500_kl.tsv";
open OUT1, ">signatures.txt";
print OUT1 "instanceid\tpaperid\tposition\tauthorname\taffiliation\tnation\tid\n";
open OUT2, ">records.txt";
print OUT2 "paperid\tvenue\tauthors\ttitle\n";


while(<INP>){
	chomp;
	if ($. == 1){
		next;
	}
	my @input = split /\t/, $_;
	
	next if $input[13] =~ /\?/;

		# column labels
		#0 isntanceid
		#1 pmcid	
		#2 pmid	
		#3 doi	
		#4 pubdate	
		#5 source	
		#6 number	
		#7 text	
		#8 software	
		#9 version	
		#10 ID	
		#11 curation_label	
		#12 mapped_to_software	
		#13 coding	
		#14 code_sb	
		#15 code_final	
		#16 note
		#17 reasoning	

	my $id = $input[13];
	if ($input[15] ne ''){
		$id = $input[15];
	}
	next if $id eq 'New';
	
	my $version = '';
	if ($input[9] ne ''){
		$version = 'y';
	}
	
	print OUT1 "$input[0]\t$input[2]\t1\t$input[8]\t$version\t\t$id\n";
	print OUT2 "$input[2]\t$input[5]\t$input[8]\t$input[7]\n";


}
close INP;
close OUT1;
close OUT2;