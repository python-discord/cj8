from setuptools import setup

required_packages = ["rich", "Pillow", "keyboard", "playsound"]

setup(
    name="pantheras_box",
    version="0.1.0",
    packages=[
        "pantheras_box",
        "pantheras_box.story",
        "pantheras_box.sounds",
        "pantheras_box.backend",
        "pantheras_box.frontend",
        "pantheras_box.networking",
        "pantheras_box.keyboard_handlers",
    ],
    url="",
    license="MIT",
    author="Patient Panthers",
    author_email="",
    description="Pantheras box TUI game.",
    install_requires=["rich", "Pillow", "keyboard", "playsound"],
    entry_points={
        "console_scripts": [
            "pantheras_box = pantheras_box.run:run_game",
        ],
    },
    package_data={"": ["**/*.txt", "**/*.yaml", "**/*.png"]},
    include_package_data=True,
)
