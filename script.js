
        document.getElementById('downloadBtn').addEventListener('click', function() {
            const link = document.createElement('a');
            link.href = 'https://www.youtube.com';  // Change this to the URL you want to download from
            link.download = 'example.txt';  // The name of the file to download
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
        