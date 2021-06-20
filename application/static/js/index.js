// document.querySelectorAll('.like-b').forEach( btn =>{
//         btn.addEventListener('click', ()=>{   
//         })
//     }
// );

// for all the like/unlike buttons, click toggle opacity, click one will cancel the other one
var likeB = document.querySelector('.like-b');
var unlikeB = document.querySelector('.unlike-b');
var liked = false;
var unliked = false;

//likeBs.forEach( likeB => {
    likeB.addEventListener('click', () =>{
        if (likeB.style.opacity == '0.5' ){
            likeB.style.opacity = '1.0';   
        }
        else{
            likeB.style.opacity = '0.5';
            unlikeB.style.opacity = '1.0';

        }
    })
//}) 

//unlikeBs.forEach( unlikeB => {
    unlikeB.addEventListener('click', () =>{
        if (unlikeB.style.opacity == '0.5'){
            unlikeB.style.opacity = '1.0';   
        }
        else{
            unlikeB.style.opacity = '0.5';
            likeB.style.opacity = '1.0';
        }
    })
//})


// ajax function 
function like(pid, flag) {
    var xhr = new XMLHttpRequest();
    xhr.open('get', '/post/'+pid+'/like', true);
    xhr.onload = () =>{
        //if (this.status == 200){
            if (flag){
                //change the cancel flag
                console.log("cancel liked");
                liked = false;
                likeB.setAttribute("onclick", "like("+pid+", 0)");
            }else{
                // confirm click
                console.log("confirm liked");
                liked = true;
                likeB.setAttribute("onclick", "like("+pid+", 1)");
                // if the post is unliked ,cancel it
                if (unliked){
                    unlike(pid, 1);
                }
            }
            window.location.href='/post/'+pid
        //}
    }
    xhr.send();
}

function unlike(pid, flag) {
    var xhr = new XMLHttpRequest();
    xhr.open('get', '/post/'+pid+'/unlike', true);
    xhr.onload = () =>{
        //if (this.status == 200){
            if (flag){
                console.log("cancel unliked");
                unliked = false;
                unlikeB.setAttribute("onclick", "unlike("+pid+", 0)");
            }else{
                // confirm click
                console.log("confirm unliked");
                unliked = true;
                unlikeB.setAttribute("onclick", "unlike("+pid+", 1)");
                // if the post is liked, cancel it
                if (liked){
                    like(pid, 1);
                }
            }
            window.location.href='/post/'+pid
        //}
    }
    xhr.send();
}


function postclick(){
    window.location.href="/post/post_experience"
}

function dailynews(){
    window.location.href="/admin/daily/news"
}

function dailytips(){
    window.location.href="/admin/daily/tips"
}

function adminwithdrawalbutton(){
    window.location.href="/admin/user_information"
}

function adminsendnotebutton(){
    window.location.href="/admin/daily/simulation_note"
}