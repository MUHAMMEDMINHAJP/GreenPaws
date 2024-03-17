

import 'package:flutter/material.dart';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:greenpaws/user_home.dart';


import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

import 'dart:convert';

import 'editprof_user.dart';





void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '',
      theme: ThemeData(

        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      // home:  (title: 'Sent Complaint'),
    );
  }
}


class userProfile_new1 extends StatefulWidget {
  const userProfile_new1({super.key, required this.title});


  final String title;

  @override
  State<userProfile_new1> createState() => _userProfile_new1State();
}
class _userProfile_new1State extends State<userProfile_new1> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    senddata();
  }



  String name='name';
  String email='email';
  String phone='phone';
  String place='place';
  String post='post';
  String pin='pin';
  String district='district';
  String gender='gender';





  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async{
        Navigator.push(context, MaterialPageRoute(builder: (context) =>UserHome(title: '',),));

        return false;

      },
      child: Scaffold(
        backgroundColor: Colors.grey.shade300,
        body:

        SingleChildScrollView(
          child: Stack(
            children: [
              SizedBox(
                height: 280,
                width: double.infinity,
                child: Image(
                  image: AssetImage("assets/a.jpg"),
                )
              ),
              Container(
                margin: EdgeInsets.fromLTRB(16.0, 240.0, 16.0, 16.0),
                child: Column(
                  children: [
                    Stack(
                      children: [
                        Container(
                          padding: EdgeInsets.all(16.0),
                          margin: EdgeInsets.only(top: 16.0),
                          decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(20.0)),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                  margin:  EdgeInsets.only(left: 110.0),
                                  child: Row(
                                    // mainAxisAlignment: MainAxisAlignment.start,
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Column(
                                        crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                        mainAxisAlignment:
                                        MainAxisAlignment.start,
                                        children: [
                                          Text(
                                            ' $name',
                                            style: Theme.of(context)
                                                .textTheme
                                                .headline6,
                                          ),
                                          // Text(
                                          //   '$email',
                                          //   style: Theme.of(context)
                                          //       .textTheme
                                          //       .bodyText1,
                                          // ),
                                          SizedBox(
                                            height: 40,
                                          )
                                        ],
                                      ),
                                      Spacer(),
                                      CircleAvatar(
                                        backgroundColor: Colors.blueAccent,
                                        child: IconButton(
                                            onPressed: () {
                                              Navigator.push(context, MaterialPageRoute(builder: (context) => MyEditPage(title: "Edit",),));
                                            },
                                            icon: Icon(
                                              Icons.edit_outlined,
                                              color: Colors.white,
                                              size: 18,
                                            )
                                        ),
                                      )
                                    ],
                                  )),
                              SizedBox(height: 10.0),
                              Row(
                                children: [

                                ],
                              ),
                            ],
                          ),
                        ),
                        // Container(
                        //   height: 90,
                        //   width: 90,
                        //   decoration: BoxDecoration(
                        //       borderRadius: BorderRadius.circular(20.0),
                        //       image:  DecorationImage(
                        //           image: NetworkImage(
                        //               photo),
                        //           fit: BoxFit.cover)),
                        //   margin: EdgeInsets.only(left: 20.0),
                        // ),
                      ],
                    ),
                    SizedBox(height: 20.0),
                    Container(
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20.0),
                      ),
                      child: Column(
                        children:  [


                          ListTile(
                            title: Text('Email'),
                            subtitle: Text(email),
                            leading: Icon(Icons.mail_outline),
                          ),
                          ListTile(
                            title: Text("Phone"),
                            subtitle: Text(phone),
                            leading: Icon(Icons.phone),
                          ),
                          ListTile(
                            title: Text('Address'),
                            subtitle: Text( '${place}  \n ${pin}\n ${post}\n ${district}\n '),
                            leading: Icon(Icons.location_city),
                          ),

                          ListTile(
                            title: Text('gender'),
                            subtitle: Text(gender),
                            leading: Icon(Icons.mail_outline),
                          ),

                          ListTile(
                            title: Text('name'),
                            subtitle: Text(name),
                            leading: Icon(Icons.mail_outline),
                          ),


                        ],
                      ),
                    )
                  ],
                ),
              ),
              Positioned(
                top: 60,
                left: 20,
                child: MaterialButton(
                  minWidth: 0.2,
                  elevation: 0.2,
                  color: Colors.white,
                  child: const Icon(Icons.arrow_back_ios_outlined,
                      color: Colors.indigo),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30.0),
                  ),
                  onPressed: () {

                    Navigator.push(context, MaterialPageRoute(builder: (context) =>UserHome(title: '',),));



                  },
                ),
              ),

            ],

          ),

        ),

      ),
    );
  }


  void senddata()async{



    SharedPreferences sh=await SharedPreferences.getInstance();
    String url=sh.getString('url').toString();
    String lid=sh.getString('lid').toString();
    final urls=Uri.parse(url+"/myapp/viewprof_user/");
    try{
      final response=await http.post(urls,body:{
        'lid':lid,
      });
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        if (status=='ok') {


          setState(() {
            gender=jsonDecode(response.body)['gender'].toString();
            email=jsonDecode(response.body)['email'].toString();
            name=jsonDecode(response.body)['name'].toString();
            phone=jsonDecode(response.body)['ph_no'].toString();
            pin=jsonDecode(response.body)['pin'].toString();
            post=jsonDecode(response.body)['post'].toString();
            place=jsonDecode(response.body)['place'].toString();
            // photo=sh.getString('img_url').toString()+jsonDecode(response.body)['photo'];
            district=jsonDecode(response.body)['district'].toString();


          });

        }else {
          Fluttertoast.showToast(msg: 'Not Found');
        }
      }
      else {
        Fluttertoast.showToast(msg: 'Network Error');
      }
    }
    catch (e){
      Fluttertoast.showToast(msg: e.toString());
    }

  }

}