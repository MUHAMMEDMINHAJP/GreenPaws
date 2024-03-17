import 'dart:convert';

import 'package:animate_do/animate_do.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:greenpaws/constants.dart';
import 'package:greenpaws/public_home.dart';
import 'package:greenpaws/signup_del.dart';
import 'package:greenpaws/signup_user.dart';
// import 'package:greenpaws/signupdel.dart';
import 'package:greenpaws/user_home.dart';
import 'package:greenpaws/user_home2.dart';
// import 'package:plantpetcare/deliveryboy/homenew.dart';
// import 'package:plantpetcare/homenew.dart';
// import 'package:plantpetcare/login.dart';
// import 'package:plantpetcare/signup.dart';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';
import 'package:greenpaws/signup_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'deliveryboy_home.dart';
import 'main.dart';

final _formkey = GlobalKey<FormState>();


void main() {
  runApp(
      const MyIndexLogin());
}

class MyIndexLogin extends StatelessWidget {
  const MyIndexLogin({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: LoginScreen(title: 'DREAM GARDEN'),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key,required this.title});
  final String title;

  static const String id = 'LoginScreen';

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool rememberMe = false;
  String username = '';
  String password = '';
  TextEditingController unamecontroller= new TextEditingController();
  TextEditingController passcontroller=new TextEditingController();


  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    setLogin();
  }

  String unm = "";
  String psw = "";
  void setLogin() async{
    SharedPreferences sh = await SharedPreferences.getInstance();
    unm =sh.getString("unm").toString();
    psw = sh.getString("psw").toString();

    unamecontroller.text = unm;
    passcontroller.text = psw;
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    return WillPopScope(
      onWillPop: ()async{
        Navigator.push(context, MaterialPageRoute(builder: (context) => Ippage(title: 'IP')));
        return false;
        },

    child: Scaffold(
        body:
        SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Container(
                height: 400,
                child: Stack(
                  children: <Widget>[
                    Positioned(
                      top: -40,
                      height: 400,
                      width: width,
                      child: FadeInUp(duration: Duration(seconds: 1), child: Container(
                        decoration: BoxDecoration(
                            image: DecorationImage(
                                image: AssetImage('assets/images/background.png'),
                                fit: BoxFit.fill
                            )
                        ),
                      )),
                    ),
                    Positioned(
                      height: 400,
                      width: width+20,
                      child: FadeInUp(duration: Duration(milliseconds: 1000), child: Container(
                        decoration: BoxDecoration(
                            image: DecorationImage(
                                image: AssetImage('assets/images/background-2.png'),
                                fit: BoxFit.fill
                            )
                        ),
                      )),
                    )
                  ],
                ),
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 40),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    FadeInUp(duration: Duration(milliseconds: 1500), child: Text("Login", style: TextStyle(color: Color.fromRGBO(49, 39, 79, 1), fontWeight: FontWeight.bold, fontSize: 30),)),
                    SizedBox(height: 30,),
                    FadeInUp(duration: Duration(milliseconds: 1700), child: Container(
                      decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(10),
                          color: Colors.white,
                          border: Border.all(color: Color.fromRGBO(196, 135, 198, .3)),
                          boxShadow: [
                            BoxShadow(
                              color: Color.fromRGBO(196, 135, 198, .3),
                              blurRadius: 20,
                              offset: Offset(0, 10),
                            )
                          ]
                      ),
                      child: Column(
                        children: <Widget>[
                          Container(
                            padding: EdgeInsets.all(10),
                            decoration: BoxDecoration(
                                border: Border(bottom: BorderSide(
                                    color: Color.fromRGBO(196, 135, 198, .3)
                                ))
                            ),
                            child: TextField(
                              controller: unamecontroller,
                              decoration: InputDecoration(
                                  border: InputBorder.none,
                                  hintText: "Username",
                                  hintStyle: TextStyle(color: Colors.grey.shade700)
                              ),
                            ),
                          ),
                          Container(
                            padding: EdgeInsets.all(10),
                            child: TextField(
                              controller: passcontroller,
                              obscureText: true,
                              decoration: InputDecoration(
                                  border: InputBorder.none,
                                  hintText: "Password",
                                  hintStyle: TextStyle(color: Colors.grey.shade700)
                              ),
                            ),
                          )
                        ],
                      ),
                    )),
                    SizedBox(height: 30,),
                    FadeInUp(duration: Duration(milliseconds: 1900), child: MaterialButton(
                      onPressed: () {
                        _send_data();
                      },
                      color: kDarkGreenColor,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(50),
                      ),
                      height: 50,
                      child: Center(
                        child: Text("Login", style: TextStyle(color: Colors.white),),
                      ),
                    )),
                    SizedBox(height: 30,),
                    FadeInUp(duration: Duration(milliseconds: 2000), child: Center(child: TextButton(onPressed: () {
                      Navigator.push(context, MaterialPageRoute(
                        builder: (context) => SignupScreen(),));
                    }, child: Text("New User Account!", style: TextStyle(color: Color.fromRGBO(49, 39, 79, .6)),)))),
                    SizedBox(height: 30,),
                    FadeInUp(duration: Duration(milliseconds: 2000), child: Center(child: TextButton(onPressed: () {
                      Navigator.push(context, MaterialPageRoute(
                        builder: (context) => DelSignup(title: 'home',),));
                    }, child: Text("New Delivery-Boy Account!", style: TextStyle(color: Color.fromRGBO(49, 39, 79, .6)),)))),
                    SizedBox(height: 30,),
                    FadeInUp(duration: Duration(milliseconds: 2000), child: Center(child: TextButton(onPressed: () {
                      Navigator.push(context, MaterialPageRoute(
                        builder: (context) => Publichome(title: 'public home',),));
                    }, child: Text("SKIP", style: TextStyle(color: Color.fromRGBO(49, 39, 79, .6)),)))),
                  ],
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  void _send_data() async{


    String uname=unamecontroller.text;
    String password=passcontroller.text;

    if (uname.isEmpty || password.isEmpty) {
      Fluttertoast.showToast(msg: 'Please fill in all fields');
    }
    else{
      SharedPreferences sh = await SharedPreferences.getInstance();
      String url = sh.getString('url').toString();

      final urls = Uri.parse('$url/myapp/loginapp/');
      try {
        final response = await http.post(urls, body: {
          'email':uname,
          'password':password,


        });
        if (response.statusCode == 200) {
          String status = jsonDecode(response.body)['status'];
          String type = jsonDecode(response.body)['type'];
          if (status=='ok') {
            if(type=="user"){
              String lid=jsonDecode(response.body)['lid'].toString();
              String name=jsonDecode(response.body)['name'].toString();
              String email=jsonDecode(response.body)['email'].toString();
              String photo=url+jsonDecode(response.body)['photo'].toString();
              sh.setString("lid", lid);
              sh.setString('name', name);
              sh.setString('email', email);
              sh.setString('photo', photo);
              Navigator.push(context, MaterialPageRoute(
                builder: (context) => UserHome2(title: "home"),));
            }
            else if(type=='delivery_boy'){
              String lid=jsonDecode(response.body)['lid'].toString();
              String name=jsonDecode(response.body)['name'].toString();
              String email=jsonDecode(response.body)['email'].toString();
              String photo=url+jsonDecode(response.body)['photo'].toString();
              sh.setString("lid", lid);
              sh.setString('name', name);
              sh.setString('email', email);
              sh.setString('photo', photo);
              Navigator.push(context, MaterialPageRoute(
                builder: (context) => DHome(title: "home"),));
            }
            else {
              Fluttertoast.showToast(msg: 'Not Found');
            }
            setState(() {
              sh.setString("unm", uname);
              sh.setString("psw", password);
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
}
