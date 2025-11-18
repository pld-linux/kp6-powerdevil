#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.3
%define		qtver		5.15.2
%define		kpname		powerdevil

Summary:	Manages the power consumption settings of a Plasma Shell
Name:		kp6-%{kpname}
Version:	6.5.3
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	b181401d45373c2454af9eb19c3ca4f1
URL:		https://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	ddcutil-devel
BuildRequires:	kf6-bluez-qt-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfig-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kidletime-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kirigami-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-knotifyconfig-devel
BuildRequires:	kf6-networkmanager-qt-devel
BuildRequires:	kf6-solid-devel
BuildRequires:	kp6-kwayland-devel
BuildRequires:	kp6-libkscreen-devel
BuildRequires:	kp6-plasma-activities-devel
BuildRequires:	kp6-plasma-workspace-devel >= %{kdeplasmaver}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Manages the power consumption settings of a Plasma Shell.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/org_kde_powerdevil
%ghost  %{_libdir}/libpowerdevilcore.so.2
%{_libdir}/libpowerdevilcore.so.*.*.*
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.backlighthelper.service
%{_datadir}/polkit-1/actions/org.kde.powerdevil.backlighthelper.policy
%{_datadir}/polkit-1/actions/org.kde.powerdevil.wakeupsourcehelper.policy
/etc/xdg/autostart/powerdevil.desktop
%{_libdir}/libpowerdevilcore.so
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.discretegpuhelper.service
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.backlighthelper.conf
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.discretegpuhelper.conf
%{systemduserunitdir}/plasma-powerdevil.service
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.chargethresholdhelper.service
%{_datadir}/dbus-1/system-services/org.kde.powerdevil.wakeupsourcehelper.service
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.chargethresholdhelper.conf
%{_datadir}/dbus-1/system.d/org.kde.powerdevil.wakeupsourcehelper.conf
%{_datadir}/polkit-1/actions/org.kde.powerdevil.chargethresholdhelper.policy
%{_datadir}/polkit-1/actions/org.kde.powerdevil.discretegpuhelper.policy
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.battery.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.brightness.so
%{_libdir}/qt6/plugins/powerdevil
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_mobile_power.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_powerdevilprofilesconfig.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/backlighthelper
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/chargethresholdhelper
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/discretegpuhelper
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/wakeupsourcehelper
%{_libdir}/qt6/plugins/kf6/krunner/krunner_powerdevil.so
%{_libdir}/qt6/qml/org/kde/plasma/private/batterymonitor
%{_libdir}/qt6/qml/org/kde/plasma/private/brightnesscontrolplugin
%{_desktopdir}/kcm_mobile_power.desktop
%{_desktopdir}/kcm_powerdevilprofilesconfig.desktop
%{_datadir}/qlogging-categories6/powerdevil.categories
%{_datadir}/knotifications6/powerdevil.notifyrc
%{_datadir}/qlogging-categories6/batterymonitor.categories
%{_datadir}/qlogging-categories6/brightness.categories
