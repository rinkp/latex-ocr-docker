import requests
from PIL import Image
import streamlit
import os
import streamlit.components.v1 as components

counter = 0

if __name__ == '__main__':
    url = os.getenv("LATEXOCR_BACKEND", "http://127.0.0.1:8502/")
    url.strip("/") # For consistent experience

    counter += 1

    streamlit.set_page_config(page_title='LaTeX-OCR')
    streamlit.title('LaTeX OCR')
    streamlit.markdown(
        """
        Convert images of equations to corresponding LaTeX code.\n\n
        This service is based on [latex-ocr-docker](https://github.com/rinkp/latex-ocr-docker) and makes use of Lukas Blecher's [pix2tex](https://github.com/lukas-blecher/LaTeX-OCR) module.\n
        [![License](https://img.shields.io/github/license/rinkp/latex-ocr-docker)](https://github.com/rinkp/latex-ocr-docker) [![issues - latex-ocr-docker](https://img.shields.io/github/issues/rinkp/latex-ocr-docker)](https://github.com/rinkp/latex-ocr-docker/issues)
        """
        )

    components.html(
        """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            parent.document.onpaste = function (event) {
                var items = (event.clipboardData  || event.originalEvent.clipboardData).items;
                console.log(JSON.stringify(items)); // will give you the mime types
                var blob = null;
                for (var i = 0; i < items.length; i++) {
                    if (items[i].type.indexOf('image') === 0) {
                    blob = items[i].getAsFile();
                    }
                }
                // if there is at least one file with image in the mime type, use the last of those
                if (blob !== null) {
                    var reader = new FileReader();
                    reader.onload = function(event) {
                        var res = event.target.result;
                    console.log(res); // data url!

                    // We need to convert the dataURL to a file
                    const file = dataURLtoFile(res, 'clipboard');
                    if (file !== null) {
                        let container = new DataTransfer(); 
                        container.items.add(file);
                        parent.document.getElementsByTagName('input')[0].files = container.files;

                        // Simulate the user picking a file because we don't have access to a lot of Javascript
                        parent.document.getElementsByTagName('input')[0].dispatchEvent(new Event('drop', { bubbles: true }));
                    }
                    };
                    reader.readAsDataURL(blob);
                }
            };
        }, false);

        // Helper function, copied from https://stackoverflow.com/a/38935990
        function dataURLtoFile(dataurl, filename) {
            var arr = dataurl.split(','),
                mime = arr[0].match(/:(.*?);/)[1],
                bstr = atob(arr[arr.length - 1]), 
                n = bstr.length, 
                u8arr = new Uint8Array(n);
            while(n--){
                u8arr[n] = bstr.charCodeAt(n);
            }
            if (mime === 'image/png') { filename = filename + '.png' }
            else if (mime === 'image/jpeg') { filename = filename + '.jpg' }
            else { return null; }
            return new File([u8arr], filename, {type:mime});
        }
        </script>
        """,
        height=0
    )

    uploaded_file = streamlit.file_uploader(
        'Upload a png or jpg containing an equation. Recognition works best if you crop the image to not include any surrounding text.\nIn modern browsers, you can also paste files or screenshots from the clipboard using CTRL+V',
        type=['png', 'jpg'],
        key="screenshot-fileupload",
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        streamlit.image(image)
    else:
        streamlit.text('\n')

    if streamlit.button('Convert'):
        if uploaded_file is not None and image is not None:
            with streamlit.spinner('Computing'):
                response = requests.post(url + '/predict/', files={'file': uploaded_file.getvalue()})
            if response.ok:
                latex_code = response.json()
                streamlit.code(latex_code, language='latex')
                streamlit.markdown(f'$\\displaystyle {latex_code}$')
            else:
                streamlit.error(response.text)
        else:
            streamlit.error('Please upload an image.')

    