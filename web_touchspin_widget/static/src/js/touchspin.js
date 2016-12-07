openerp.web_touchspin_widget=function(instance,module)
{
	var QWeb = instance.web.qweb;
	var _t = instance.web._t;

	instance.web.form.widgets = instance.web.form.widgets.extend(
	{
		'touchspin' : 'instance.web.form.Fieldtouchspin',
	});
    	    
    instance.web.form.Fieldtouchspin = instance.web.form.FieldChar.extend({
    template: 'Fieldtouchspin',
    initialize_content: function() {
        this._super();
        var $button = this.$el.find('button');
        $button.click(this.on_button_clicked);
        this.setupFocus($button);
    },
    get_options: function(){
    		options= {
					min: 0, 
					max: 100, 
					initval: '',
					replacementval: '',
					decimals: 0,
					forcestepdivisibility: 'round', 
					verticalbuttons: false,
					verticalupclass: 'glyphicon glyphicon-chevron-up',
					verticaldownclass: 'glyphicon glyphicon-chevron-down',
					boostat: 5, 
					booster: true,
					maxboostedstep: 10, 
					//postfix: '%', 
					//prefix: '$', 
					prefix_extraclass: '',
					postfix_extraclass: '',
					step: 1, 
					stepinterval: 100, 
					stepintervaldelay: 500,
					mousewheel: true,
					buttondown_class: 'btn btn-default',
					buttonup_class: 'btn btn-default',
					buttondown_txt: '-',
					buttonup_txt: '+'
						};
		var opt2=this.options;
		if (opt2.min!=undefined)
			options.min = opt2.min
		if (opt2.max!=undefined)
			options.max = opt2.max
		if (opt2.initval!=undefined)
			options.initval = opt2.initval
		if (opt2.decimals!=undefined)
			options.decimals = opt2.decimals
		if (opt2.postfix!=undefined)
			options.postfix = opt2.postfix
		if (opt2.prefix!=undefined)
			options.prefix = opt2.prefix
		if (opt2.step!=undefined)
			options.step = opt2.step
		if (opt2.buttondown_txt!=undefined)
			options.buttondown_txt = opt2.buttondown_txt
		if (opt2.buttonup_txt!=undefined)
			options.buttonup_txt = opt2.buttonup_txt
		return options
    },
    render_value: function() {
		

        if (!this.get("effective_readonly")) {
            this._super();
this.$el.find('input').TouchSpin(this.get_options());
        
        } else {
            this._super();


        }
    },
    on_button_clicked: function() {
        if (!this.get('value')) {
            this.do_warn(_t("Resource Error"), _t("This resource is empty"));
        } else {
            var url = $.trim(this.get('value'));
            if(/^www\./i.test(url))
                url = 'http://'+url;
            window.open(url);
        }
    }
});

}