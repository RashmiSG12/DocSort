const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');

let uploadedFile = null;

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const file = e.dataTransfer.files[0];
  handleFile(file);
});

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  handleFile(file);
});

function handleFile(file) {
  if (file && file.type === 'application/pdf') {
    uploadedFile = file;
    fileName.textContent = `Selected: ${file.name}`;
    fileName.classList.add('show');
  } else {
    fileName.textContent = '❌ Only PDF files are supported.';
    fileName.classList.add('show');
    uploadedFile = null;
  }
}

uploadBtn.addEventListener('click', () => {
  if (!uploadedFile) {
    fileName.textContent = '❌ No file selected.';
    return;
  }

  fileName.textContent = '⏳ Uploading and organizing...';
  fileName.classList.add('show');

  const formData = new FormData();
  formData.append('file', uploadedFile);

  fetch('http://127.0.0.1:8000/upload-pdf/', {
    method: 'POST',
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      fileName.textContent = `✅ File organized into: ${data.label}`;
      uploadedFile = null;
    })
    .catch(err => {
      fileName.textContent = `❌ Error uploading file.`;
      console.error(err);
    });
});

// Show files in category on click
document.querySelectorAll('.category-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const category = link.querySelector('.category-text').textContent.toLowerCase();
    fetch(`http://127.0.0.1:8000/list-files/${category}`)
      .then(res => res.json())
      .then(data => {
        if (data.files.length === 0) {
          alert(`No files in ${category}`);
        } else {
          alert(`Files in ${category}:\n\n` + data.files.join('\n'));
        }
      })
      .catch(err => {
        alert('Failed to fetch files.');
        console.error(err);
      });
  });
});
