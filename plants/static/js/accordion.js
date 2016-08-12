jQuery('.accordion').accordion({ collapsible:true, active:false, autoHeight:         false, disabled:true});
jQuery('.accordion >.panel panel-default').click(function(){
      jQuery(this).next().slideToggle();
});
jQuery('.accordion-expand-all').click(function(){
      jQuery('#accordion h3.ui-accordion-header').next().slideDown();
});
