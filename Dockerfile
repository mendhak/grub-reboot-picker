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
               dh-python python3-all lintian python3-hatchling pybuild-plugin-pyproject \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*

RUN python3 --version


WORKDIR /build/grub-reboot-picker

COPY . /build/grub-reboot-picker

ARG version
ARG suite


RUN python3 other/generate_changelog.py 

RUN dpkg-parsechangelog -l debian/changelog 

RUN dpkg-buildpackage -uc -us

WORKDIR /build

# Run a lint against this deb
RUN lintian grub-reboot-picker_${version}_all.deb
# Look at information about this deb
RUN dpkg -I grub-reboot-picker_${version}_all.deb
# Look at the contents of this deb
RUN dpkg -c grub-reboot-picker_${version}_all.deb