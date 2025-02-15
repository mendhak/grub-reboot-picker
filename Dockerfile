FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

RUN set -ex \
    && sed -i -- 's/# deb-src/deb-src/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
               build-essential \
               cdbs \
               devscripts \
               equivs \
               fakeroot \
               dh-python python3-all python3-setuptools python3-hatchling pybuild-plugin-pyproject \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*

RUN python3 --version


WORKDIR /build

COPY . /build

ARG version
ARG suite


RUN cd debian_build 

RUN python3 generate_changelog.py 

RUN dpkg-parsechangelog -l debian/changelog 

RUN dpkg-buildpackage -uc -us

# # Run a lint against this deb
RUN lintian deb_dist/grub-reboot-picker_$version_all.deb
# # Look at information about this deb
RUN dpkg -I deb_dist/grub-reboot-picker_$version_all.deb

RUN dpkg -c deb_dist/grub-reboot-picker_$version_all.deb