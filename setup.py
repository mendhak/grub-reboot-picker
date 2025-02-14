from setuptools import setup

setup(
    name="grub-reboot-picker",
    version="0.0.1",
    author="Mendhak",
    author_email="mendhak@users.noreply.github.com",
    description="Tray application, reboot into different OSes.",
    url="https://github.com/mendhak/grub-reboot-picker",
    packages=['src'],
    include_package_data=True,
    python_requires='>=3.6',
)