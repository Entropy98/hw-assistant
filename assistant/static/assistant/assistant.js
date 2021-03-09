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
    $(lists).each(function(){
      categories = Object.keys(this);
      for(var i=0; i<categories.length; i++){
        let grocery_id = categories[i]+"-grocery-list"
        let stock_id = categories[i]+"-stock-list"
        let elem = document.getElementById(grocery_id)
        if(elem != null){elem.remove()}
        elem = document.getElementById(stock_id)
        if(elem != null){elem.remove()}
      }
    })
  })

  $(lists).each(function(){
    categories = Object.keys(this);
    for(var i=0; i<categories.length; i++){
      let category = categories[i];
      items = Object.keys(this[category]);
      let list_id = category+'-grocery-list'
      if(document.getElementById(list_id) == null){
        checklist = '<ul id="'+list_id+'">'
        for(var j=0; j<items.length; j++){
          let item = items[j];
          let quantity = this[category][item]
          if(quantity < 0){
            checklist += '<li id="'+category+'-item-'+j+'">'+
                            formatItem(item) +' x'+ (-1*quantity) +'</li>';
          }
        }
        checklist += '</ul>';
        category_id = '#'+list_id+'-label';
        $(category_id).after(checklist);
      }
      list_id = category+'-stock-list'
      if(document.getElementById(list_id) == null){
        checklist = '<ul id="'+list_id+'">'
        for(var j=0; j<items.length; j++){
          let item = items[j];
          let quantity = this[category][item]
          if(quantity > 0){
            checklist += '<li id="'+category+'-item-'+j+'">'+
                            formatItem(item) +' x'+ quantity +'</li>';
          }
        }
        checklist += '</ul>';
        category_id = '#'+list_id+'-label';
        $(category_id).after(checklist);
      }
    }
  })
}

function formatItem(item){
  var stringArray = item.split(' ');
  let retval = '';
  for(var i=0; i<stringArray.length; i++){
    let word = stringArray[i];
    if(word != ''){
      retval += word.charAt(0).toUpperCase() + word.slice(1) + ' ';
    }
  }
  return retval
}
