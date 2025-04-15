function openModal(){
    let modal = document.getElementById("modal-user");
    modal.style.display = "block";
}

function closeModal(){
    let modal = document.getElementById("modal-user");
    modal.style.display = "none";
}

console.log(document.getElementsByTagName('*') );

let profileInput = document.getElementById("profile_picture");
console.log(document.getElementById("profile_picture"));
profileInput.addEventListener("onchange",function(){
    console.log(profileInput.files[0]);
});

window.onclick = function(event) {
    let modal = document.getElementById("modal-user");
    if (event.target == modal){
        modal.style.display = "none";
    }
} 