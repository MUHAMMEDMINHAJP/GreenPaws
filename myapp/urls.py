
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [

#admin
    path('login/', views.login),
    path('login_post/', views.login_post),
    path('adminhome/',views.adminhome),
    path('signup/', views.signup),
    path('signup_post/', views.signup_post),
    path('verifyshop/', views.verifyshop),
    path('verifyshop_post/', views.verifyshop_post),
    path('approvedshops/', views.approvedshop),
    path('approvedshop_post/',views.approvedshop_post),
    path('rejectshop/', views.rejectedshop),
    path('rejectedshop_post/',views.rejectedshop_post),
    path('verifydel/', views.verifydel),
    path('verifydel_post/', views.verifydel_post),
    path('approvedel/<id>', views.approvedel),
    path('rejectdel/<id>', views.rejectdel),
    path('approve/<id>',views.approve),
    path('reject/<id>',views.reject),
    path('approveddel/', views.approveddel),
    path('approveddel_post/', views.approveddel_post),
    path('rejecteddel/', views.rejecteddel),
    path('rejecteddel_post/', views.rejecteddel_post),
    path('admin_viewreviews/', views.admin_viewreviews),


#Plant Shop
    path('shop_prof/', views.shop_prof),
    path('shop_editprof/', views.shop_editprof),
    path('shop_editprof_post/', views.shop_editprof_post),
    path('addplant/', views.addplant),
    path('addplant_post/',views.addplant_post),
    path('viewplant/', views.viewplant),
    path('viewplant_post/', views.viewplant_post),
    path('details/<id>', views.details),
    path('details_post/', views.details_post),
    path('plantstock/', views.plantstock),
    path('plantstock_post/', views.plantstock_post),
    path('viewplantstock/', views.viewplantstock),
    path('viewplantstock_post/', views.viewplantstock_post),

    path('plantshop_assigndel/<id>', views.plantshop_assigndel),
    path('plantshop_assigndel_post/', views.plantshop_assigndel_post),

    path('shop_viewassigneddel/<id>',views.shop_viewassigneddel),


#changepassword
    path('plant_changepass/',views.plant_changepass),
    path('plant_changepass_post/',views.plant_changepass_post),
    path('pet_changepass/',views.pet_changepass),
    path('pet_changepass_post/',views.pet_changepass_post),
    path('app_changepass/',views.app_changepass),



#Pet Shop
    path('shophome/', views.shophome),
    path('delplant/<id>', views.delplant),
    path('editplant/<id>', views.editplant),
    path('editplant_post/', views.editplant_post),
    path('logout/', views.logout),
    path('back_phome/', views.back_phome),

    path('petshophome/', views.petshophome),
    path('addpet/', views.addpet),
    path('addpet_post/', views.addpet_post),
    path('viewpet/', views.viewpet),
    path('delpet/<id>', views.delpet),
    path('editpet/<id>', views.editpet),
    path('editpet_post/', views.editpet_post),
    path('viewpet_post/', views.viewpet_post),
    path('petshop_prof/', views.petshop_prof),
    path('petshop_editprof/', views.petshop_editprof),
    path('petshop_editprof_post/', views.petshop_editprof_post),
    path('petstock/', views.petstock),
    path('petstock_post/', views.petstock_post),
    path('viewpetstock/', views.viewpetstock),
    path('viewpetstock_post/', views.viewpetstock_post),


    path('user_makepetpayment/', views.user_makepetpayment),
    path('user_makepetpaymentto/', views.user_makepetpaymentto),
# userhome
    path('loginapp/', views.loginapp),
    path('signup_user/', views.signup_user),
    path('viewprof_user/', views.viewprof_user),
    path('ediprof_user/', views.ediprof_user),
    path('viewdef_address_user/', views.viewdef_address_user),
    path('viewdef_alladdress_user/', views.viewdef_alladdress_user),
        # plant
    path('user_viewplantshops/', views.user_viewplantshops),
    path('user_viewshopplant/', views.user_viewshopplant),
    path('viewsingleplant/', views.user_viewsingleplant),
    path('user_viewplant/', views.user_viewplant),
    path('user_viewoneplant/', views.user_viewoneplant),
    path('user_addplantcart/', views.user_addplantcart),
    path('userhome_addplantcart/', views.userhome_addplantcart),
    path('viewplantcart/', views.viewplantcart),
    path('addplant_quantitycart/', views.addplant_quantitycart),
    path('delcart/', views.delcart),

    path('user_viewmyorder/', views.user_viewmyorder),
    path('user_viewmyordermore/', views.user_viewmyordermore),
    path('user_cancelmyorder/', views.user_cancelmyorder),
    path('userpet_viewmyorder/', views.userpet_viewmyorder),
    path('userpet_viewmyordermore/', views.userpet_viewmyordermore),

    path('add_plantreview/', views.add_plantreview),
    path('user_viewreviews/', views.user_viewreviews),

    path('shop_viewreviews/', views.shop_viewreviews),


#add to cart
    path('userhome_addpetcart/', views.userhome_addpetcart),

    #search
    path('plantshop_search/', views.plantshop_search),
    path('petshop_search/', views.petshop_search),

    # path('add_petreview/', views.add_petreview),




    path('plantshop_assigndel/<id>', views.plantshop_assigndel),
    path('plantshop_assigndel_post/', views.plantshop_assigndel_post),

    # pet
    path('user_viewpetshops/', views.user_viewpetshops),
    path('user_viewshoppet/', views.user_viewshoppet),
    path('user_viewpet/', views.user_viewpet),
    path('user_viewonepet/', views.user_viewonepet),
    path('viewpetcart/', views.viewpetcart),
    path('user_viewsinglepet/', views.user_viewsinglepet),
    path('user_addpetcart/', views.user_addpetcart),
    path('addpet_quantitycart/', views.addpet_quantitycart),
    path('delpetcart/', views.delpetcart),


    #address
    path('add_address/', views.add_address),
    path('user_makepayment/', views.user_makepayment),
    path('viewaddress_user/', views.viewaddress_user),
    path('editaddress_user/', views.editaddress_user),
    path('viewprof_user_address/', views.viewprof_user_address),
    path('user_makepaymentto/', views.user_makepaymentto),



    #order
    path('plantshop_vieworders/', views.plantshop_vieworders),
    path('plantshop_vieworders_post/', views.plantshop_vieworders_post),
    path('plantshop_vieworders_more/<id>', views.plantshop_vieworders_more),





#public

    path('public_viewoneplant/', views.public_viewoneplant),

#delivery Boy
    path('signup_del/', views.signup_del),
    path('viewprof_del/', views.viewprof_del),
    path('ediprof_del/', views.ediprof_del),
    path('viewassigned_delboy/', views.viewassigned_delboy),
    path('del_updatestatus/', views.del_updatestatus),
    path('view_deliveredorder/', views.view_deliveredorder),
    path('del_editdeldate/', views.del_editdeldate),

#disease prediction
    path('upload_file/', views.upload_file),


#bill generation
    path('generate_bill_pdf/', views.generate_bill_pdf),
    path('generate_pdf_bill_payment/<pid>', views.generate_pdf_bill_payment),
    path('user_generate_pdf_bill_payment/', views.user_generate_pdf_bill_payment),



]