//generic filter of elements
function filterElements(input) {
    let inp = input.value.toLowerCase();
    let table = document.querySelectorAll(".table")[0];
    let rows = table.tBodies[0].children;
    for (let i = 0; i < rows.length; i++){
        if (inp.length == 0)
            rows[i].style.display = "table-row";
        else {
            let columns = rows[i].children;
            for (let j = 0; j < columns.length; j++){
                if (columns[j].textContent.toLowerCase().includes(inp)){
                    rows[i].style.display = "table-row";
                    break;
                }
                else
                    rows[i].style.display = "none";
            }
        }
    }
}

//zoom image
function zoomImage(img) {
    let modalImg = document.querySelector("#imgmodal");
    modal.style.display = "block";
    modalImg.src = img.src;
}

function closeModal() {
    let modal = document.querySelector("#modal");
    modal.style.display = "none";
}