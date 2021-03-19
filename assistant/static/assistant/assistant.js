function removeItem(item){
  let name = item.id.substring("remove-".length);
  name = ' '+name.replaceAll('-',' ');
  $.ajax({
    url: '/remove_grocery',
    type: 'POST',
    data: 'grocery='+name+'&quantity=0',
    dataType: 'json',
    success: updateLists,
    error: updateError
  });
}

function storeItem(item){
  let name = item.id.substring("store-".length);
  name = ' '+name.replaceAll('-',' ');
  $.ajax({
    url: '/store_grocery',
    type: 'POST',
    data: 'grocery='+name+'&quantity=0',
    dataType: 'json',
    success: updateLists,
    error: updateError
  });
}

function repeatItem(item){
  let name = item.id.substring("buy-again-".length);
  name = ' '+name.replaceAll('-',' ');
  $.ajax({
    url: '/repeat_grocery',
    type: 'POST',
    data: 'grocery='+name+'&quantity=0',
    dataType: 'json',
    success: updateLists,
    error: updateError
  });
}

function toggleMenu(){
  let menu = document.getElementById('nav-menu');
  if(menu.style.display == 'none'){
    menu.style.display = 'inline-block';
  }
  else{
    menu.style.display = 'none';
  }
}

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
            checklist +=  '<hr>'+
                          '<li id="'+category+'-item-'+j+'">'+
                            formatItem(item) +' x'+ (-1*quantity) + '  '+
                            '<i onclick="removeItem(this)" class="far fa-times-circle remove-btn"'+
                            'id="remove-'+formatItemId(item)+'"></i>'+
                            '<i onclick="storeItem(this)" class="far fa-check-circle store-btn"'+
                            'id="store-'+formatItemId(item)+'"></i>'+
                          '</li>';
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
            checklist +=  '<hr>'+
                          '<li id="'+category+'-item-'+j+'">'+
                            formatItem(item) +' x'+ quantity +'  '+
                            '<i onclick="removeItem(this)" class="far fa-times-circle remove-btn"'+
                            'id="remove-'+formatItemId(item)+'"></i>'+
                            '<i onclick="repeatItem(this)" class="fas fa-redo buy-again-btn"'+
                            'id="buy-again-'+formatItemId(item)+'"></i>'+
                          '</li>';
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

function formatItemId(item){
  var stringArray = item.split(' ');
  let retval = '';
  for(var i=0; i<stringArray.length; i++){
    let word = stringArray[i];
    if(word != ''){
      retval += word;
      if(i != stringArray.length-1){
        retval += '-';
      }
    }
  }
  return retval
}
