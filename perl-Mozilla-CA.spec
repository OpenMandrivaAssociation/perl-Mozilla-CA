%define upstream_name    Mozilla-CA
%define upstream_version 20130114

Name:		perl-%{upstream_name}
Version:	%perl_convert_version %{upstream_version}
Release:	4

Summary:	Mozilla's CA cert bundle in PEM format
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{upstream_name}
Source0:	http://www.cpan.org/modules/by-module/Mozilla/%{upstream_name}-%{upstream_version}.tar.gz

BuildRequires:	perl-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test)
BuildArch:	noarch

%description
Mozilla::CA provides a copy of Mozilla's bundle of Certificate Authority
certificates in a form that can be consumed by modules and libraries based
on OpenSSL.

The module provide a single function:

* SSL_ca_file()

%prep
%setup -q -n %{upstream_name}-%{upstream_version}

%build
perl Makefile.PL INSTALLDIRS=vendor
%make

%check
%make test

%install
%makeinstall_std

%files
%doc Changes META.json META.yml MYMETA.yml README
%{_mandir}/man3/*
%{perl_vendorlib}/*

