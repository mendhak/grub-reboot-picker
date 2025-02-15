FROM ubuntu:22.04

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
               python3-stdeb fakeroot python3-all dh-python lintian devscripts \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*

RUN python3 --version


WORKDIR /build

COPY . /build

ARG version
ARG suite

# Create the source and deb
RUN python3 setup.py --command-packages=stdeb.command sdist_dsc --suite $suite bdist_deb
# # Run a lint against this deb
RUN lintian deb_dist/grub-reboot-picker_$version-1_all.deb
# # Look at information about this deb
RUN dpkg -I deb_dist/grub-reboot-picker_$version-1_all.deb

RUN dpkg -c deb_dist/grub-reboot-picker_$version-1_all.deb