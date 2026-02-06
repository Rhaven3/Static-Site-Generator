# [Static Site Generator](https://rhaven3.github.io/Static-Site-Generator/) (SSG) for [Boot.dev](https://www.boot.dev/u/rhaven)

A lightweight static site generator built in Python as part of my Boot.dev training. This project allowed me to practice unit testing, implement a complex project from scratch, and solidify my understanding of Python.

![SSG_final](https://github.com/user-attachments/assets/c9f5d532-9691-45d9-b354-864dd4858860)

**Live Demo:** [GitHub Pages](https://rhaven3.github.io/Static-Site-Generator/)

**Markdown Sources:** [Markdown Files](https://github.com/Rhaven3/Static-Site-Generator/tree/main/content)

---

## ✨ Features

- **Markdown to HTML:** Convert `.md` files to static HTML pages.
- **Unit Tested:** Comprehensive test suite for core functionality.

---

## 🎓 Learning Outcomes

- **Unit Testing:** Wrote and maintained tests for all critical components.
- **Project Structure:** Organized a complex project with clear separation of concerns.
- **Python Skills:** Applied OOP, file I/O.


---

## 🚀 Deploy on Github Pages

1. Create a Github Repositories (not very optional)
2. Create some Markdown content in ``/content``
   - if you want some CSS style in ``/static/css``
   - and for the image in  ``/static/images``

3.  launch in terminal to generate your website
   ```bash
python3 src/main.py "/REPO_NAME/"
```

4. Open your repository's settings on GitHub and select Pages in the Code and automation section to config the publishing source.
   - Set the source to the main branch and the docs directory.
   - Save the settings.
   - (Now the /docs directory on your main branch will auto deploy to your GitHub Pages URL once something is in it.)
5. Commit and push your changes to GitHub

6. Open the live URL (https://USERNAME.github.io/REPO_NAME/) in your browser and ensure that the site is live and working correctly. You can check the status and find the exact URL in the GitHub Pages section of your repository settings.

## 🧪 Testing and Local Deploy (only available in Unix)

Test with unit test in ``test_*.py`` file
```bash
./test.sh
```

Local deploy in ``/public``
```bash
./main.sh
```


  


