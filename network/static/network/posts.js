document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.getElementById('profile_view_btn').addEventListener('click', () => show_current_view('profile_view'));
    document.getElementById('posts_view_btn').addEventListener('click', () => show_current_view('posts_view'));
    document.getElementById('following_posts_btn').addEventListener('click', () => show_current_view('posts_view', "following"));

    show_default_page();

    //TEST
    document.getElementById('test_btn').addEventListener('click', () => test_function());
});

function test_function(){
    console.log("Test button");
    fetch('/test')
      .then(test_response => test_response.json())
      .then(test_data =>  {
        console.log(test_data);
        console.log(test_data.author);
        console.log(test_data.content);
        console.log(test_data.timestamp);
      })
      .catch(error => console.error(error));

}


function highlight_selected_item(btn) {
    const profileButton = document.getElementById('profile_view_btn');
    profileButton.classList.remove("selected_item");

    const feedButton = document.getElementById('posts_view_btn');
    feedButton.classList.remove("selected_item");

    const following_posts = document.getElementById('following_posts_btn');
    following_posts.classList.remove("selected_item");

    const selected_item = document.getElementById(btn);
    selected_item.classList.add("selected_item")
}

function show_current_view(view, type = "all") {

    console.log(view, type);
    // Show compose view and hide other views
    document.getElementById('posts_view').style.display = 'none';
    document.getElementById('profile_view').style.display = 'none';
    const current_view = document.getElementById(view);
    current_view.style.display = 'block';
    current_view.innerHTML = '';

    if (view == 'profile_view') {
        show_profile(current_view)
    }
    else if (view == 'posts_view') {
        show_feed(current_view, type)

    }
}

function show_profile(current_view) {
    highlight_selected_item('profile_view_btn');
    current_view.innerHTML = `
        <h1>Profile</h1>
    `

    // fetch(`/profile`)
    // .then(response => response.json())
    // .then(emails => {
    //     //iterate over emails received on Json
    //     emails.forEach(email => {
    //         const element = document.createElement('div');
    //         const read_style = !email.read? '\"': 'list-group-item-dark\"';

    //         console.log(read_style);
    //         element.innerHTML = `
    //                   <a href="#" class="list-group-item list-group-item-action ${read_style}  aria-current="true" >
    //                       <div class="d-flex w-100 justify-content-between">
    //                           <h5>${email.subject}</h5>
    //                           <small >${email.timestamp}</small>
    //                       </div>
    //                         <p class="mb-1">${email.body}</p>
    //                         <small>${email.sender}</small>
    //                   </a>

    //         `
    //         element.addEventListener('click', () => get_mail(email.id));
    //         document.querySelector('#emails-view').append(element);
    //     });
    // // ... do something else with emails ...
    // });

}

function show_default_page() {
    show_current_view('posts_view');
}

function show_feed(current_view, feed_type) {
    if (feed_type == 'all') {
        highlight_selected_item('posts_view_btn');
        current_view.innerHTML = `
            <h1>All Posts</h1>
        `
    }
    else if (feed_type == 'following') {
        highlight_selected_item('following_posts_btn');
        current_view.innerHTML = `
            <h1>Following Posts</h1>
        `
    }
}