import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="size_comparisons",  # Replace with your own username
    version="0.0.1",
    author="Daan Alkemade",
    author_email="author@example.com",
    description="Package for thesis Daan Alkemade",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
)
