#
# Conditional build:
%bcond_without	gnome_shell	# GNOME Shell extension
#
Summary:	Clipboard management system
Summary(pl.UTF-8):	System zarządzania schowkiem
Name:		gpaste
Version:	3.36.3
Release:	2
License:	BSD
Group:		X11/Applications
Source0:	http://www.imagination-land.org/files/gpaste/%{name}-%{version}.tar.xz
# Source0-md5:	3bd71852b7a0fe9a94994698c38c91e6
Patch0:		%{name}-sh.patch
URL:		https://github.com/Keruspe/GPaste
BuildRequires:	appstream-glib-devel
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.15
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gdk-pixbuf2-devel >= 2.38.0
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	gjs-devel >= 1.54.0
BuildRequires:	glib2-devel >= 1:2.58
BuildRequires:	gobject-introspection-devel >= 1.58.0
BuildRequires:	gtk+3-devel >= 3.24
BuildRequires:	libtool >= 2:2.2.6
%{?with_gnome_shell:BuildRequires:	mutter-devel >= 3.36}
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.29
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.42
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	gpaste-applet < 3.20
Suggests:	wgetpaste >= 2.26
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gpasted is a clipboard management daemon with DBus interface.
gpaste-client is its CLI client and gpaste-settings is a tool to edit
gpasted settings.

%description -l pl.UTF-8
gpasted to demon zarządzający schowkiem przy użyciu interfejsu DBus.
gpaste-client to klient linii poleceń, a gpaste-settings to narzędzie
do modyfikowania ustawień.

%package libs
Summary:	Library to manage the clipboard history
Summary(pl.UTF-8):	Biblioteka do zarządzania historią schowka
Group:		Libraries
Requires:	gdk-pixbuf2 >= 2.38.0
Requires:	glib2 >= 1:2.58
Requires:	gtk+3 >= 3.24

%description libs
libgpaste is a library to manage the clipboard history (used by
gpasted).

%description libs -l pl.UTF-8
libgpaste to biblioteka do zarządzania historią schowka
(wykorzystywana przez gpasted).

%package devel
Summary:	Development files for libgpaste library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libgpaste
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gdk-pixbuf2-devel >= 2.38.0
Requires:	glib2-devel >= 1:2.58
Requires:	gtk+3-devel >= 3.24

%description devel
This package contains the header files for developing applications
that use libgpaste library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libgpaste.

%package -n vala-gpaste
Summary:	Vala API for libgpaste library
Summary(pl.UTF-8):	API języka Vala do biblioteki libgpaste
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.42

%description -n vala-gpaste
Vala API for libgpaste library.

%description -n vala-gpaste -l pl.UTF-8
API języka Vala do biblioteki libgpaste.

%package -n gnome-shell-extension-%{name}
Summary:	GNOME Shell extension for GPaste
Summary(pl.UTF-8):	Rozszerzenie powłoki GNOME (GNOME Shell) dla GPaste
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-shell >= 3.36
BuildArch:	noarch

%description -n gnome-shell-extension-%{name}
GNOME Shell extension for GPaste.

%description -n gnome-shell-extension-%{name} -l pl.UTF-8
Rozszerzenie powłoki GNOME (GNOME Shell) dla GPaste.

%package -n bash-completion-%{name}
Summary:	Bash completion for GPaste commands
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów poleceń GPaste
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-%{name}
Bash completion for GPaste commands.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie parametrów poleceń GPaste.

%package -n zsh-completion-%{name}
Summary:	ZSH completion for GPaste commands
Summary(pl.UTF-8):	Dopełnianie parametrów ZSH dla poleceń GPaste
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n zsh-completion-%{name}
zsh completion for GPaste commands.

%description -n zsh-completion-%{name} -l pl.UTF-8
Dopełnianie parametrów ZSH dla poleceń GPaste.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_gnome_shell:--disable-gnome-shell-extension} \
	--disable-schemas-compile \
	--disable-silent-rules \
	--enable-vala \
	--with-controlcenterdir=%{_datadir}/gnome-control-center/keybindings \
	--with-systemduserunitdir=%{systemduserunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# Install bash/zsh completion support
install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p data/completions/gpaste-client $RPM_BUILD_ROOT%{bash_compdir}
install -d $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
cp -p data/completions/_gpaste-client $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{nl_NL,nl}

%find_lang GPaste

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/org.gnome.GPaste.Ui.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f GPaste.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README.md THANKS TODO
%attr(755,root,root) %{_bindir}/gpaste-client
%{_mandir}/man1/gpaste-client.1*
%dir %{_libexecdir}/gpaste
%attr(755,root,root) %{_libexecdir}/gpaste/gpaste-daemon
%attr(755,root,root) %{_libexecdir}/gpaste/gpaste-ui
%{systemduserunitdir}/org.gnome.GPaste.service
%{systemduserunitdir}/org.gnome.GPaste.Ui.service
%{_datadir}/dbus-1/services/org.gnome.GPaste.service
%{_datadir}/dbus-1/services/org.gnome.GPaste.Ui.service
%{_datadir}/glib-2.0/schemas/org.gnome.GPaste.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*-gpaste.xml
%{_datadir}/metainfo/org.gnome.GPaste.Ui.appdata.xml
%{_desktopdir}/org.gnome.GPaste.Ui.desktop

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpaste.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpaste.so.11
%{_libdir}/girepository-1.0/GPaste-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpaste.so
%{_datadir}/gir-1.0/GPaste-1.0.gir
%{_includedir}/gpaste
%{_pkgconfigdir}/gpaste-1.0.pc

%files -n vala-gpaste
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gpaste-1.0.deps
%{_datadir}/vala/vapi/gpaste-1.0.vapi

%files -n gnome-shell-extension-%{name}
%defattr(644,root,root,755)
%{_datadir}/gnome-shell/extensions/GPaste@gnome-shell-extensions.gnome.org
%{_datadir}/gnome-shell/search-providers/org.gnome.GPaste.search-provider.ini

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/gpaste-client

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_gpaste-client
