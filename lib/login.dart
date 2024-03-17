import 'package:flutter/material.dart';
import 'package:greenpaws/signup_del.dart';
import 'package:greenpaws/signup_user.dart';
import 'package:greenpaws/user_home.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:fluttertoast/fluttertoast.dart';

import 'deliveryboy_home.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const Loginpage(title: 'Flutter Demo Home Page'),
    );
  }
}

class Loginpage extends StatefulWidget {
  const Loginpage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<Loginpage> createState() => _LoginpageState();
}

class _LoginpageState extends State<Loginpage> {
  TextEditingController EmailController =TextEditingController();
  TextEditingController PasswordController =TextEditingController();

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(

        backgroundColor: Theme.of(context).colorScheme.inversePrimary,

        title: Text(widget.title),
      ),
      body: Center(

        child: Column(

          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextFormField(controller:EmailController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Email'),),

            TextFormField(controller:PasswordController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Password'),),
            ElevatedButton(onPressed: (){

              senddata();
            }, child: Text('login')),
            // Text('Already have a account!'),
            Row(children: [SizedBox(width: 10,), Text('Already have a account!'),  SizedBox(width: 2,) ,
              ElevatedButton(onPressed: (){
              Navigator.push(context, MaterialPageRoute(builder: (context)=>UserSignup(title: ''),));
            }, child: Text('signup'))

            ],) ,Row(children: [SizedBox(width: 10,), Text('Already have a account!'),  SizedBox(width: 2,) ,
              ElevatedButton(onPressed: (){
              Navigator.push(context, MaterialPageRoute(builder: (context)=>DelSignup(title: ''),));
            }, child: Text('delivery boy signup'))

            ],)
            //
          ],
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: _incrementCounter,
      //   tooltip: 'Increment',
      //   child: const Icon(Icons.add),
      // ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
  void senddata()async{
    String Email=EmailController.text;
    String Password=PasswordController.text;
    SharedPreferences  sh= await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();

    final urls = Uri.parse('$url/myapp/loginapp/');
    try {
      final response = await http.post(urls, body: {
        'email':Email,
        'password':Password,


      });
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        String type = jsonDecode(response.body)['type'];
        if (status=='ok') {
          if (type == 'user') {
            String lid = jsonDecode(response.body)['lid'];
            sh.setString("lid", lid);

            Navigator.push(context, MaterialPageRoute(
              builder: (context) => UserHome(title: "Home"),));
          } if (type == 'delivery_boy') {
            String lid = jsonDecode(response.body)['lid'];
            sh.setString("lid", lid);

            Navigator.push(context, MaterialPageRoute(
              builder: (context) => DHome(title: "Home"),));
          }
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


