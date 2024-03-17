import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:greenpaws/login.dart';
import 'package:greenpaws/viewpetshops.dart';
import 'package:greenpaws/viewplants.dart';
import 'package:greenpaws/viewprofile.dart';
import 'package:greenpaws/viewshops.dart';


import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';


import 'package:shared_preferences/shared_preferences.dart';

import 'login_screen.dart';
void main() {
  runApp(const HomeNew());
}

class HomeNew extends StatelessWidget {
  const HomeNew({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Home',
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Color.fromARGB(255, 18, 82, 98)),
        useMaterial3: true,
      ),
      home: const UserHome(title: 'Home'),
    );
  }
}

class UserHome extends StatefulWidget {
  const UserHome({super.key, required this.title});

  final String title;

  @override
  State<UserHome> createState() => _UserHomeState();
}

class _UserHomeState extends State<UserHome> {


  // _UserHomeState() {
  //   view_notification();
  // }

  List<String> id_ = <String>[];
  List<String> name_= <String>[];
  List<String> department_= <String>[];
  List<String> gender_= <String>[];
  List<String> place_= <String>[];
  List<String> phone_= <String>[];
  List<String> photo_= <String>[];


  Future<void> view_notification() async {
    List<String> id = <String>[];
    List<String> name = <String>[];
    List<String> department = <String>[];
    List<String> gender = <String>[];
    List<String> place = <String>[];
    List<String> phone = <String>[];
    List<String> photo = <String>[];


    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String url = '$urls/myapp/user_viewdoctors/';

      var data = await http.post(Uri.parse(url), body: {


      });
      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {
        id.add(arr[i]['id'].toString());
        name.add(arr[i]['name']);
        department.add(arr[i]['department']);
        gender.add(arr[i]['gender']);
        place.add(arr[i]['place']);
        phone.add(arr[i]['phone']);
        photo.add(urls+ arr[i]['photo']);

      }

      setState(() {
        id_ = id;
        name_ = name;
        department_ = department;
        gender_ = gender;
        place_ = place;
        phone_ = phone;
        photo_ =  photo;
      });

      print(statuss);
    } catch (e) {
      print("Error ------------------- " + e.toString());
      //there is error during converting file image to base64 encoding.
    }
  }







  String uname_="";
  String email_="";
  String uphoto_="";


  _UserHomeState()
  {

    a();
    view_notification();

  }

  a()
  async {
    SharedPreferences sh = await SharedPreferences.getInstance();
    String imgurl=sh.getString('img_url').toString();
    String name = sh.getString('name').toString();
    String email = sh.getString('email').toString();
    String photo = imgurl+sh.getString('photo').toString();


    setState(() {
      uname_=name;
      email_=email;
      uphoto_=photo;

    });


  }


  TextEditingController unameController = new TextEditingController();
  TextEditingController passController = new TextEditingController();

  @override
  Widget build(BuildContext context) {

    return WillPopScope(
      onWillPop: () async{ return true; },
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Color.fromARGB(255, 18, 82, 98),

          title: Text(widget.title),
        ),
        body:
        Container(
          decoration: const BoxDecoration(
            image: DecorationImage(
                image: AssetImage(''), fit: BoxFit.cover),
          ),
          child: GridView(
            gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
              maxCrossAxisExtent: 210,
              childAspectRatio: 10 / 10,
              crossAxisSpacing: 10,
              mainAxisSpacing: 10,
            ),
            padding: const EdgeInsets.all(8.0),
            children: [
              Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(207, 28, 62, 100),
                      borderRadius: BorderRadius.circular(15)),
                  child: Column(children: [
                    SizedBox(height: 5.0),
                    InkWell(
                      child: CircleAvatar(
                          radius: 50,
                          backgroundImage: NetworkImage(
                              'https://images.unsplash.com/photo-1634718669030-b80bcf4e7e5b?q=80&w=1820&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')),
                      onTap: () {Navigator.push(context, MaterialPageRoute(
                        builder: (context) => viewshopspage(title: 'shops',),));},
                    ),
                    SizedBox(height: 30.0),
                    // CircleAvatar(radius: 50,backgroundImage: NetworkImage(photo_[index])),
                    Column(
                      children: [
                        Padding(
                          padding: EdgeInsets.all(1),
                          child: Text("View Plant Shop",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              )),
                        ),
                      ],
                    ),
                  ])),
              Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(207, 28, 62, 100),
                      borderRadius: BorderRadius.circular(15)),
                  child: Column(children: [
                    SizedBox(height: 5.0),
                    InkWell(
                      child: CircleAvatar(
                          radius: 50,
                          backgroundImage: NetworkImage(
                              'https://images.unsplash.com/photo-1628158186246-3d94c73cddee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NjB8fHBldHNob3B8ZW58MHx8MHx8fDA%3D')),
                      onTap: () {Navigator.push(context, MaterialPageRoute(
                       builder: (context) => viewpetshops(title:'petshops',),));},
                    ),
                    SizedBox(height: 30.0),
                    // CircleAvatar(radius: 50,backgroundImage: NetworkImage(photo_[index])),
                    Column(
                      children: [
                        Padding(
                          padding: EdgeInsets.all(1),
                          child: Text("View Pet Shops",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              )),
                        ),
                      ],
                    ),
                  ])),
              Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(207, 28, 62, 100),
                      borderRadius: BorderRadius.circular(15)),
                  child: Column(children: [
                    SizedBox(height: 5.0),
                    InkWell(
                    //
                      child: CircleAvatar(
                          radius: 50,
                          backgroundImage: NetworkImage('https://th.bing.com/th/id/OIP._dF3h309digWf96LoMjMfwHaGu?rs=1&pid=ImgDetMain')
                      ),
                     onTap: () {Navigator.push(context, MaterialPageRoute(
                        builder: (context) => viewplants(title: ""),));},
                    ),
                    SizedBox(height: 30.0),
                    // CircleAvatar(radius: 50,backgroundImage: NetworkImage(photo_[index])),
                    Column(
                      children: [
                        Padding(
                          padding: EdgeInsets.all(1),
                          child: Text("View Plants",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              )),
                        ),
                      ],
                    ),
                  ])),
              Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(207, 28, 62, 100),
                      borderRadius: BorderRadius.circular(15)),
                  child: Column(children: [
                    SizedBox(height: 5.0),
                    // InkWell(
                    //
                    //   child: CircleAvatar(
                    //       radius: 50,
                    //       backgroundImage: NetworkImage('https://i.pinimg.com/originals/fa/ec/50/faec5006f1a3cc2210a70313c0954367.jpg')
                    //   ),
                    //   onTap: () {
                    //     Navigator.push(context, MaterialPageRoute(
                    //     builder: (context) => LoginPage(title: "",),));},
                    // ),
                    SizedBox(height: 30.0),
                    // CircleAvatar(radius: 50,backgroundImage: NetworkImage(photo_[index])),
                    Column(
                      children: [
                        Padding(
                          padding: EdgeInsets.all(1),
                          child: Text("View Pets",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                              )),
                        ),
                      ],
                    ),
                  ])),
            ],
          ),
        ),


        drawer: Drawer(
          child: ListView(
            padding: EdgeInsets.zero,
            children: [
              DrawerHeader(
                decoration: BoxDecoration(
                  color: Color.fromARGB(255, 18, 82, 98),
                ),
                child:
                Column(children: [

                  Text(
                    'IN HOME',
                    style: TextStyle(fontSize: 20,color: Colors.white,fontStyle:FontStyle.italic,fontWeight: FontWeight.bold),

                  ),
                  CircleAvatar(radius: 29,backgroundImage: NetworkImage(uphoto_)),
                  Text(uname_,style: TextStyle(color: Colors.white)),
                  Text(email_,style: TextStyle(color: Colors.white)),



                ])


                ,
              ),
              ListTile(
                leading: Icon(Icons.home),
                title: const Text('Home'),
                onTap: () {
                  Navigator.pop(context);
                  Navigator.push(context, MaterialPageRoute(builder: (context) => HomeNew(),));
                },
              ),
              ListTile(
                leading: Icon(Icons.person_pin),
                title: const Text(' View Profile '),
                onTap: () {
                  Navigator.pop(context);
                  Navigator.push(context, MaterialPageRoute(builder: (context) => userProfile_new1(title: 'USer Profile',),));
                },
              ),
              // ListTile(
              //   leading: Icon(Icons.production_quantity_limits_outlined),
              //   title: const Text(' View Shops '),
              //   onTap: () {
              //
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => viewshops(title: "Booking Details",),));
              //   },
              // ),
              // // ListTile(
              // //   leading: Icon(Icons.category),
              // //   title: const Text(' View Category '),
              // //   onTap: () {
              // //     // Navigator.pop(context);
              // //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewDoctors(title: "Doctors",),));
              // //   },
              // // ),
              // ListTile(
              //   leading: Icon(Icons.production_quantity_limits_outlined),
              //   title: const Text(' View Pets and Plants '),
              //   onTap: () {
              //
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewBookingDetailsPage(title: "Booking Details",),));
              //   },
              // ),
              // ListTile(
              //   leading: Icon(Icons.note_alt_rounded),
              //   title: const Text('View Pets '),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewPrescriptionPage(title: "Prescription Details",),));
              //   },
              // ),
              // ListTile(
              //   leading: Icon(Icons.shopping_cart_sharp),
              //   title: const Text(' View Plants'),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewTestDetailsPage(title: "Test Details",),));
              //   },
              // ),
              // ListTile(
              //   leading: Icon(Icons.shopping_cart_sharp),
              //   title: const Text(' View Cart'),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewTestDetailsPage(title: "Test Details",),));
              //   },
              // ),


              // ListTile(
              //   leading: Icon(Icons.local_pharmacy),
              //   title: const Text(' View Pharmacy '),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewPharmacy(title: "Pharmacy",),));
              //   },
              //
              // ),

              // ListTile(
              //   leading: Icon(Icons.medical_information_outlined),
              //   title: const Text(' View Medicine Orders '),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewMedicineOrderPage(title: "Medicine Order Details",),));
              //   },
              // ),
              ListTile(
                leading: Icon(Icons.feed_outlined),
                title: const Text(' My Orders'),
                onTap: () {
                  // Navigator.pop(context);
                  // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewCart(),));
                },
              ),
              // ListTile(
              //   leading: Icon(Icons.feed_outlined),
              //   title: const Text('Complaint '),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewReplyPage(title: "View Complaint",),));
              //   },
              // ),
              // ListTile(
              //   leading: Icon(Icons.reviews_outlined),
              //   title: const Text('Review '),
              //   onTap: () {
              //     // Navigator.pop(context);
              //     // Navigator.push(context, MaterialPageRoute(builder: (context) => ViewReplyPage(title: "View Complaint",),));
              //   },
              // ),

              ListTile(
                leading: Icon(Icons.change_circle),
                title: const Text(' Change Password '),
                onTap: () {
                  // Navigator.pop(context);
                  // Navigator.push(context, MaterialPageRoute(builder: (context) => MyChangePasswordPage(title: "Change Password",),));
                },
              ),
              ListTile(
                leading: Icon(Icons.logout),
                title: const Text('LogOut'),
                onTap: () {

                   Navigator.push(context, MaterialPageRoute(builder: (context) => LoginScreen(title: '',),));
                },
              ),
            ],
          ),
        ),





      ),
    );
  }



// void _send_data() async{
//
//
//   String uname=unameController.text;
//   String password=passController.text;
//
//
//   SharedPreferences sh = await SharedPreferences.getInstance();
//   String url = sh.getString('url').toString();
//
//   final urls = Uri.parse('$url/myapp/user_loginpost/');
//   try {
//     final response = await http.post(urls, body: {
//       'name':uname,
//       'password':password,
//
//
//     });
//     if (response.statusCode == 200) {
//       String status = jsonDecode(response.body)['status'];
//       if (status=='ok') {
//         String lid=jsonDecode(response.body)['lid'];
//         sh.setString("lid", lid);
//         Navigator.push(context, MaterialPageRoute(
//           builder: (context) => MyHomePage(title: "Home"),));
//       }else {
//         Fluttertoast.showToast(msg: 'Not Found');
//       }
//     }
//     else {
//       Fluttertoast.showToast(msg: 'Network Error');
//     }
//   }
//   catch (e){
//     Fluttertoast.showToast(msg: e.toString());
//   }
// }

}