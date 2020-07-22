$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
      }
    }
  }
  );
  $('input').each((_index, input) => input.checked = false)  

// Display Comments and Replies
  $('.view-comments-btn').click(function(){
    $('.comment-card').show();
    $('.view-comments-btn').hide();
  });

// Close Sidemenu when clicking outsite
  $('.sidebarMenuInner').click((e) => {
    if ($(e)[0].originalEvent.target.dataset.toggle) { return }
    $('input').each((_index, input) => input.checked = false)
    $('#sidebarOverlay').hide();
  } ) 

// Comments and Replies handler
assingHandlers = () => {
  $('.reply-button').click(e => {
    $(e.target).parents('.card-body').find('.reply-form').toggle()
  });
  
  $('.reply-button').click(e => {
    if ($(e.target).parents('.card-body').find('.reply-form').innerHTML === 'View');
    console.log('ello')
  });

  $('.comment-btn').click(function(){
    $('#comment-form').toggle();
    $('.view-comments-btn').hide();
  });

  $('.view-replies-btn').click(e => {
    $(e.target).parents('.card-body').find('.reply-section').toggle()
    const replyBtn = $(e.target)

    replyBtn.html(
      replyBtn.html() === 'View' ? 'Hide' : 'View'
   )

  });

};

assingHandlers();

// Comments
$(document).on('submit', '#comment-form', function(event){
  event.preventDefault();
  const slug = $('#slug').first().data('slug');
  const data = {
    content: $(event.target).find('.form-control').val()
   }

  $.ajax({
    method: 'POST',
    url: `/post/${slug}/`,
    data: data,
    dataType: 'json',
    success: function(response) {
      $('#comment-form').toggle();
      $('.main-comment-section').html(response['form']);
      assingHandlers();
      $('textarea').val('');
    },
    error: function(rs, e) {
      console.log(rs.responseText);
    },
  })
})

// Replies
$(document).on('submit', '.reply-form', function(event){
  const slug = $('#slug').first().data('slug');

  event.preventDefault();
  const data = {
  comment_id: $(event.target).find('.reply-comment-id').val(),
  content: $(event.target).find('.form-control').val()
 }

  $.ajax({
    method: 'POST',
    url: `/post/${slug}/`,
    data: data,
    dataType: 'json',
    success: function(response) {
      $(event.target).parents('.reply-form').hide()
      $('.main-comment-section').html(response['form']);
      assingHandlers();
      $('textarea').val('');
    },
    error: function(rs, e) {
      console.log(rs.responseText);
    },
  })
  event.preventDefault();
})

// Likes
$(document).on('click', '#like', function(event){
  event.preventDefault();
  var pk = $(this).attr('value');
  const slug = $('#slug').first().data('slug');

  $.ajax({
    method: 'POST',
    url: `/post/${slug}/like/`,
    data: {'slug' : pk},
    dataType: 'json',
    success: function(response) {
      $('.like-section').html(response['form']);
    },
    error: function(rs, e) {
      console.log(rs.responseText);
    },
  })
  event.preventDefault();
})

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function getCSRFToken()
{
  return getCookie('csrftoken');
}

});