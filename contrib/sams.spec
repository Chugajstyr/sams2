%define samsrelease nil
Summary: SAMS (Squid Account Management System)
Name: sams
Version: 1.0.4
Release: 0
Group: Applications/Internet
License: GPL
Source: http://nixdev.net/release/sams/%{name}-%{version}.tar.bz2
Patch0: sams-1.0.4.rpm.patch
Distribution: Red Hat Linux
Vendor: Sams community
Packager: Pavel Vinogradov <Pavel.Vinogradov@nixdev.net>
URL: http://sams.perm.ru
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: mysql-devel, pcre-devel
Requires: mysql >= 3.23, php >= 4.3.2, httpd, squid, pcre

%description
This program basically used for administrative purposes of squid proxy.
There are access control for users by ntlm, ncsa, basic or ip
authorization mode.

%description -l ru
Этот пакет используется для администрирования прокси-сервера Squid.
С установокой этого пакета доступны возможноси по управлению трафиком
пользователей и авторизацией по схемам ntlm, ncsa, basic or ip.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%build
%configure \
	--prefix=/usr \
	%ifarch x86_64
	--with-mysql-libpath=/usr/lib64/mysql/ \
	--with-pcre-libpath=/usr/lib64/ \
	%endif #x86_64    
	--with-configfile=%{_sysconfdir}/sams.conf \
	--with-rcd-locations=%{_sysconfdir}/rc.d/init.d \
	--with-httpd-locations=%{_var}/www/html

make

%install
#rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{_var}/www/html

%makeinstall \
	RCDPATH=$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d \
	HTTPDPATH=$RPM_BUILD_ROOT%{_var}/www/html
rm -f $RPM_BUILD_ROOT%{_var}/www/html/sams

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG INSTALL* README*
%doc doc/img
%lang(en) %doc doc/EN
%lang(ru) %doc doc/RU
%config(noreplace) %{_sysconfdir}/sams.conf
%{_bindir}/*
%{_datadir}/sams
%attr(777,root,root) %dir %{_datadir}/sams/data
%{_sysconfdir}/rc.d/init.d/sams

%pre
if [ "$1" = 2 ] ; then
    /sbin/service samsd stop || /sbin/service sams stop
fi
exit 0

%post
if [ "$1" = 1 ] ; then
ln -s %{_datadir}/sams %{_var}/www/html/
/sbin/chkconfig --add sams
/sbin/chkconfig --level 345 sams on
fi

if [ "$1" = 2 ] ; then
    echo Warning: you are upgrading existing sams package.
    echo Please run %{_datadir}/sams/data/upgrade_mysql_table.php manually.
    echo This is strongly recommended to ensure your sams tables is up to date.
fi
exit 0

%preun
if [ "$1" = 0 ] ; then 
/sbin/service sams stop
/sbin/chkconfig --del sams
fi
exit 0

%postun
rm -f %{_var}/www/html/sams
exit 0

%changelog
* Fri Nov 14 2008 Pavel Vinogradov <Pavel.Vinogradov@nixdev.net> 1.0.4
Small build fixed and grammar corection
New upstream version 1.0.4

* Sat Nov 8 2008 Denis Zagirov <foomail@yandex.ru> 1.0.3
Credit patch  by cj_nik added.

* Fri Oct 31 2008 Denis Zagirov <foomail@yandex.ru>
Path to /usr/lib64 added for x86_64 added to configure stage.

* Thu Oct 30 2008 Denis Zagirov <foomail@yandex.ru>
Stages added: pre post preun postun 
service name changed to 'sams'
Dealing with /var/www/html/sams moved to post and postun section
Added pcre-devel in to Buildrequire section
Added mysql tables upgrade warning

* Fri Jul 25 2008 Denis Zagirov <foomail@yandex.ru>
Fixed simlink to %{_datadir}/sams
Workaround for moving old sams.conf, ensure not to move sams.conf during rpm
build on host with working sams. (Makefile.am lines 200-203 out)

* Thu Jun 16 2005 Dmitry Chemerik <chemerik@mail.ru>
New version