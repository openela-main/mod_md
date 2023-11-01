# Module Magic Numberfa
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}

Name:           mod_md
Version:        2.0.8
Release:        8%{?dist}
Summary:        Certificate provisioning using ACME for the Apache HTTP Server
License:        ASL 2.0
URL:            https://icing.github.io/mod_md/
Source0:        https://github.com/icing/mod_md/releases/download/v%{version}/mod_md-%{version}.tar.gz
# documentation
Source10:       a2md.xml
Patch1:         mod_md-2.0.8-state_dir.patch
Patch2:         mod_md-2.0.8-duptrim-seg.patch
Patch3:         mod_md-2.0.8-tolerate-missing-res.patch
BuildRequires:  gcc
BuildRequires:  pkgconfig, httpd-devel >= 2.4.37, openssl-devel >= 1.1.0, jansson-devel, libcurl-devel
BuildRequires:  xmlto
Requires:       httpd-mmn = %{_httpd_mmn}, mod_ssl >= 1:2.4.37-17
Conflicts:      httpd < 2.4.37-17
Epoch:          1

%description
This module manages common properties of domains for one or more
virtual hosts. Specifically it can use the ACME protocol to automate
certificate provisioning.  Certificates will be configured for managed
domains and their virtual hosts automatically, including at renewal.

%prep
%setup -q
%patch1 -p1 -b .state_dir
%patch2 -p1 -b .dup_trim
%patch3 -p1 -b .tol_missing_res

xmlto man $RPM_SOURCE_DIR/a2md.xml

%build
%configure
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build V=1

%check
%make_build check

%install
%make_install
rm -rf %{buildroot}/etc/httpd/share/doc/

# remove links and rename SO files
rm -f %{buildroot}%{_httpd_moddir}/mod_md.so
mv %{buildroot}%{_httpd_moddir}/mod_md.so.0.0.0 %{buildroot}%{_httpd_moddir}/mod_md.so

# create configuration
mkdir -p %{buildroot}%{_httpd_modconfdir}
echo "LoadModule md_module modules/mod_md.so" > %{buildroot}%{_httpd_modconfdir}/01-md.conf

# Install man pages
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p a2md.1 $RPM_BUILD_ROOT%{_mandir}/man1

%files
%doc README.md ChangeLog AUTHORS
%license LICENSE
%config(noreplace) %{_httpd_modconfdir}/01-md.conf
%{_httpd_moddir}/mod_md.so
%{_bindir}/a2md
%{_mandir}/man1/*

%changelog
* Thu May 28 2020 Lubos Uhliarik <luhliari@redhat.com> - 1:2.0.8-8
- Resolves: #1832844 - mod_md does not work with ACME server that does not
  provide keyChange or revokeCert resources

* Wed Jan 22 2020 Lubos Uhliarik <luhliari@redhat.com> - 1:2.0.8-7
- Resolves: #1747912 - add a2md(1) documentation

* Mon Dec 09 2019 Lubos Uhliarik <luhliari@redhat.com> - 1:2.0.8-6
- Resolves: #1781263 - mod_md ACMEv1 crash

* Thu Oct 03 2019 Lubos Uhliarik <luhliari@redhat.com> - 1:2.0.8-5
- Resolves: #1747898 - add mod_md package

* Fri Aug 30 2019 Joe Orton <jorton@redhat.com> - 1:2.0.8-4
- require mod_ssl, update package description

* Fri Aug 30 2019 Joe Orton <jorton@redhat.com> - 1:2.0.8-3
- rebuild against 2.4.41

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Joe Orton <jorton@redhat.com> - 1:2.0.8-1
- update to 2.0.8

* Tue Jun 11 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.0.3-1
- Initial import (#1719248).
