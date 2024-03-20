// add a function to delete a Note from the database by it's id
function deleteNote(noteId) {
    fetch('/notes/delete', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = '/';
    });
}