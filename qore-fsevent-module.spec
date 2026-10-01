# Copyright (C) 2026 Qore Technologies, s.r.o.
# SPDX-License-Identifier: MIT
# Use the pinned source epoch for RPM headers and installed file timestamps.
%global source_date_epoch_from_changelog 1
%global use_source_date_epoch_as_buildtime 1
%if v"%{rpmversion}" >= v"4.20"
%global build_mtime_policy clamp_to_source_date_epoch
%else
%global clamp_mtime_to_source_date_epoch 1
%endif
%bcond_without tests
%bcond_without docs
Name: qore-fsevent-module
Version: 2.0.0
Release: 1%{?dist}
Summary: File system event monitoring for Qore
License: MIT AND Zlib AND LicenseRef-Fedora-Public-Domain
URL: https://github.com/qoretechnologies/module-fsevent
Source0: %{name}-%{version}.tar.xz
%global _find_debuginfo_dwz_opts %{nil}
BuildRequires: cmake >= 3.21
BuildRequires: make
BuildRequires: gcc-c++
%if %{with tests}
BuildRequires: python3 >= 3.11
%endif
Provides: bundled(efsw)
BuildRequires: qore-devel >= 3.0.0~
BuildRequires: qore-rpm-macros >= 3.0.0~
%if %{with docs}
BuildRequires: doxygen
BuildRequires: /usr/bin/hardlink
%endif
%{?qore_enable_aot_post}

%description
Native file system watching using the bundled Entropia File System Watcher,
with Qore interfaces for event polling and event delivery.

%if %{with docs}
%package doc
Summary: File system event module reference documentation
BuildArch: noarch
%description doc
API reference and examples for Qore's file system event module.
%endif

%prep
%autosetup
%build
%{?set_build_flags}
. %{_rpmconfigdir}/qore/module-env.sh
qore_set_source_prefix_maps "%{qore_debug_source_dir}"
cmake -S . -B build -G 'Unix Makefiles' \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
  -DCMAKE_SKIP_RPATH=ON -DCMAKE_IGNORE_PREFIX_PATH=/usr/local \
  -DQore_DIR=%{_libdir}/cmake/Qore -DQORE_EXECUTABLE=/usr/bin/qore \
  -DQORE_QPP_EXECUTABLE=/usr/bin/qpp -DQORE_QCC_EXECUTABLE=/usr/bin/qcc \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DQORE_BUILD_AOT_MODULES=ON -DQORE_AOT_LINK_SOURCE_MODULES=OFF \
  -DQORE_QM_METADATA_ENV:STRING="QORE_MODULE_DIR=$QORE_MODULE_DIR:$PWD/qlib;QORE_MODULE_DIR_ONLY=1;QORE_INCLUDE_DIR=;LD_LIBRARY_PATH=" \
  -DCMAKE_DISABLE_FIND_PACKAGE_Doxygen=%{!?with_docs:ON}%{?with_docs:OFF}
cmake --build build -- %{?_smp_mflags}
%if %{with docs}
cmake --build build --target docs -- %{?_smp_mflags}
%endif
%install
DESTDIR=%{buildroot} cmake --install build
%qore_install_aot_sources qlib
find %{buildroot}%{_libdir}/qore-modules -type f -name '*.qmod' -exec chmod 755 {} +
%if %{with docs}
install -d %{buildroot}%{_docdir}/%{name}-doc
cp -a build/docs %{buildroot}%{_docdir}/%{name}-doc/
hardlink -t -O %{buildroot}%{_docdir}/%{name}-doc
%endif
%check
%if %{with tests}
. %{_rpmconfigdir}/qore/module-env.sh
python3 -B -W error -m unittest discover -s test -p test_realpath.py -v
for test in test/*.qtest; do
  timeout 180 /usr/bin/qore -b --enable-debug \
    -l "$PWD/build/fsevent-api-$(/usr/bin/qore --latest-module-api).qmod" \
    -l "$PWD/build/qlib-qmod/FsEventPollerUtil.qmod" \
    -l "$PWD/build/qlib-qmod/FsEventPoller.qmod" "$test" -v
done
%endif
%files
%license debian/copyright
%doc README
%{_libdir}/qore-modules/fsevent-api-*.qmod
%{_libdir}/qore-modules/FsEventPoller.qmod
%{_libdir}/qore-modules/FsEventPollerUtil.qmod
%{_datadir}/qore-modules/FsEventPoller.qm
%{_datadir}/qore-modules/FsEventPollerUtil.qm
%dir %{_datadir}/qore/metadata/fsevent
%{_datadir}/qore/metadata/fsevent/*.meta.json
%if %{with docs}
%files doc
%license debian/copyright
%doc %{_docdir}/%{name}-doc/
%endif
%changelog
* Thu Oct 01 2026 David Nichols <david@qore.org> - 2.0.0-1
- Package native and AOT event modules with offline tests and bundled notices.
