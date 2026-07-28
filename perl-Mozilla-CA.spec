%define upstream_name    Mozilla-CA
Name:		perl-%{upstream_name}
Version:	20250602
Release:	4

Summary:	Mozilla's CA cert bundle in PEM format
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		https://github.com/libwww-perl/Mozilla-CA
Source0:	https://cpan.metacpan.org/authors/id/L/LW/LWP/Mozilla-CA-%{version}.tar.gz
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test)
BuildRequires:	perl(Test::More)
BuildRequires:	perl-Test-Simple
Requires: ca-certificates
BuildArch:	noarch

%description
Mozilla::CA provides a copy of Mozilla's bundle of Certificate Authority
certificates in a form that can be consumed by modules and libraries based
on OpenSSL.

The module provide a single function:

* SSL_ca_file()

%prep
%setup -q -n %{upstream_name}-%{version}
# Redirect SSL_ca_file() to system ca-certificates bundle
cat > lib/Mozilla/CA.pm << 'CAEOF'
package Mozilla::CA;
use strict;
use warnings;

our $VERSION = '20250602';

use File::Spec ();

sub SSL_ca_file {
    return File::Spec->catfile('/etc/pki/tls/certs/ca-bundle.crt');
}

1;
CAEOF
# Exclude bundled cacert.pem from packaging
cat >> Makefile.PL << 'MFEOF'

package MY;
sub libscan {
    my $name = shift->SUPER::libscan(@_);
    if ($name =~ /cacert\.pem\z/) { $name = '' }
    return $name;
}
MFEOF
# Do not ship Mozilla downloader scripts
rm -f mk-ca-bundle.pl maint/mk-ca-bundle.pl 2>/dev/null || true
sed -i '/mk-ca-bundle.pl/d' MANIFEST 2>/dev/null || true

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make

%check
%make test

%install
%makeinstall_std

%files
%doc Changes README
%{_mandir}/man3/*
%{perl_vendorlib}/*

