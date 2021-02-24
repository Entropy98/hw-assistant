function getLists(){
  $.ajax({
    url: '/update_lists',
    dataType: 'json',
    success: updateLists,
    error: updateError
  });
}

function updateError(xhr, status, error){
  displayError('Status='+xhr.status+' ('+error+')')
}

function displayError(message){
  document.getElementById('error').innerHTML = message
}

function updateLists(lists){
  $("ul").each(function(){
    let category = this.id.substring("-list".length)
    $(lists).each(function(){
    })
  })

  $(lists).each(function(){
    categories = Object.keys(this);
    for(var i=0; i<categories.length; i++){
      let category = categories[i];
      items = Object.keys(this[category]);
      let list_id = category+'-list'
      if(document.getElementById(list_id) == null){
        checklist = '<ul id="'+list_id+'">'
        for(var j=0; j<items.length; j++){
          let item = items[j];
          checklist += '<li id="'+category+'-item-'+j+'">'+
                          item+' x'+this[category][item]+'</li>';
        }
        checklist += '</ul>';
        let category_id = '#'+category+'-list-label';
        console.log(category_id)
        $(category_id).after(checklist);
      }
    }
  })
}
