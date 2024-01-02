# pix2tex - LaTeX OCR
[![GitHub](https://img.shields.io/github/license/lukas-blecher/LaTeX-OCR)](https://github.com/lukas-blecher/LaTeX-OCR) 

This is a fork of [lukas-blecher/LaTeX-OCR](https://github.com/lukas-blecher/LaTeX-OCR) for enhanced usability with  Docker. For detailed usage instructions, see the original repository. 

## Usage
This repository contains a `docker-compose.yml` file to get you started quickly. 

1. Either build the containers yourself using `docker compose build` or pull the containers from Dockerhub: `docker compose pull`
2. Run both `docker compose up -d`
3. Navigate to [localhost:8501](http://localhost:8501) to use the frontend

By default, the api service port is not published and is only accessible to the frontend. Add the [`ports`](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports) attribute to that service to make port 8501 available. If you only want to use the api, you can remove the frontend.
  
## Acknowledgment
This is a fork of [lukas-blecher/LaTeX-OCR](https://github.com/lukas-blecher/LaTeX-OCR) who acknowledged the following people:

Code taken and modified from [lucidrains](https://github.com/lucidrains), [rwightman](https://github.com/rwightman/pytorch-image-models), [im2markup](https://github.com/harvardnlp/im2markup), [arxiv_leaks](https://github.com/soskek/arxiv_leaks), [pkra: Mathjax](https://github.com/pkra/MathJax-single-file), [harupy: snipping tool](https://github.com/harupy/snipping-tool)

### Fonts

Latin Modern Math, `GFSNeohellenicMath.otf`, Asana Math, XITS Math, Cambria Math

