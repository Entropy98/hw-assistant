function showDropdown(){
  document.getElementById("dropdown-content").classList.toggle("show");
}

window.onclick = function(event){
  if(!event.target.matches('.dropdownbtn')){
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for( var i=0; i<dropdowns.length; i++){
      var openDropdown = dropdowns[i];
      if(openDropdown.classList.contains('show')){
        openDropdown.classList.remove('show');
      }
    }
  }
}

function toggleMissingIngr(recipe){
  document.getElementById(recipe+"_missing_list").classList.toggle("show");
  document.getElementById(recipe+"_ingredients_list").classList.remove("show");
  document.getElementById(recipe+"_optional_list").classList.remove("show");
}

function toggleIngr(recipe){
  document.getElementById(recipe+"_missing_list").classList.remove("show");
  document.getElementById(recipe+"_ingredients_list").classList.toggle("show");
  document.getElementById(recipe+"_optional_list").classList.remove("show");
}

function toggleOptionalIngr(recipe){
  document.getElementById(recipe+"_missing_list").classList.remove("show");
  document.getElementById(recipe+"_ingredients_list").classList.remove("show");
  document.getElementById(recipe+"_optional_list").classList.toggle("show");
}

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
  let button = document.getElementById('nav-button');
  let button_mobile = document.getElementById('nav-button-mobile');
  if(menu.style.display == 'none'){
    menu.style.display = 'inline-block';
    button.innerHTML = '<i class="fas fa-times"></i>';
    button_mobile.innerHTML = '<i class="fas fa-times"></i>';
  }
  else{
    menu.style.display = 'none';
    button.innerHTML = '<i class="fas fa-bars"></i>';
    button_mobile.innerHTML = '<i class="fas fa-bars"></i>';
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

function updateNumIngredients(){
  numIngr = document.getElementById('num_ingredients').value;
  ingredients = document.getElementsByClassName('ingredient_input');
  ingrBreaks = document.getElementsByClassName('ingredient_br');
  prevNumIngr = -1;
  for(var i=0; i<ingredients.length; i++){
    index = parseInt(ingredients[i].id.substring("ingredient_input_".length));
    if(index > prevNumIngr){
      prevNumIngr = index;
    }
  }
  while(ingredients.length>numIngr){
    ingredients[0].remove();
    ingrBreaks[0].remove();
  }
  input = '';
  for(var i=prevNumIngr+1; i<numIngr; i++){
    input +=  '<input type="text" class="ingredient_input" id="ingredient_input_'+i+'" name="ingredient_input_'+i+'">'+
              '<br class="ingredient_br">';
  }
  $('#ingredients_break').after(input);
}

function updateNumOptions(){
  numIngr = document.getElementById('num_options').value;
  ingredients = document.getElementsByClassName('option_input');
  ingrBreaks = document.getElementsByClassName('option_br');
  prevNumIngr = -1;
  for(var i=0; i<ingredients.length; i++){
    index = parseInt(ingredients[i].id.substring("option_input_".length));{
    if(index > prevNumIngr)
      prevNumIngr = index;
    }
  }
  while(ingredients.length>numIngr){
    ingredients[0].remove();
    ingrBreaks[0].remove();
  }
  input = '';
  for(var i=prevNumIngr+1; i<numIngr; i++){
    input +=  '<input type="text" class="option_input" id="option_input_'+i+'" name="option_input_'+i+'">'+
              '<br class="option_br">';
  }
  $('#options_break').after(input);
}

function selectRecipe(recipe){
  $.ajax({
    url: '/select_recipe',
    type: 'POST',
    data: 'recipe='+recipe+
          '&csrfmiddlewaretoken='+getCSRFToken(),
    dataType: 'json',
    success: updateRecipe,
    error: updateError
  });
}

function updateRecipe(recipe){
  data = recipe[0];
  document.getElementById('recipe_name').value = data.name;
  document.getElementById('recipe_shortname').value = data.shortname;
  radios = document.getElementsByClassName('radio_btn');
  for(var i=0; i<radios.length; i++){
    radios[i].checked = false;
  }
  document.getElementById(data.category).checked = true;
  document.getElementById('num_ingredients').value = data.ingredients.length;
  document.getElementById('num_options').value = data.options.length;
  updateNumIngredients();
  updateNumOptions();
  for(var i=0; i<data.ingredients.length; i++){
    document.getElementById('ingredient_input_'+i).value = data.ingredients[i];
  }
  for(var i=0; i<data.options.length; i++){
    document.getElementById('option_input_'+i).value = data.options[i];
  }
}

function getCSRFToken(){
  let cookies = document.cookie.split(";")
  for (let i=0; i< cookies.length; i++){
    let c = cookies[i].trim()
    if(c.startsWith("csrftoken=")){
      return c.substring("csrftoken=".length, c.length)
    }
  }
  return "unknown"
}

