import 'package:flutter/material.dart';
import 'package:greenpaws/login.dart';
import 'package:greenpaws/login_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

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
      home: const Ippage(title: 'Flutter Demo Home Page'),
    );
  }
}

class Ippage extends StatefulWidget {
  const Ippage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<Ippage> createState() => _IppageState();
}

class _IppageState extends State<Ippage> {
  TextEditingController IpController =TextEditingController();
  final formkey = GlobalKey<FormState>();




  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(

        backgroundColor: Theme.of(context).colorScheme.inversePrimary,

        title: Text(widget.title),
      ),
      body: Center(

        child: Form(
          key:formkey,
          child: Column(

            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              TextFormField(
                validator: (value){
                  if(value!.isEmpty){
                    return "Please Fill";
                  }
                  return null;
                },
                controller:IpController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'ip address'),),
              ElevatedButton(onPressed: (){
                if(formkey.currentState!.validate()){
                  senddata();

                }
              }, child: Text('login'))
              //
            ],
          ),
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
    String ip =IpController.text;
    SharedPreferences  sh= await SharedPreferences.getInstance();
    sh.setString('url', "http://"+ip+":8000");
    sh.setString('imgurl', "http://"+ip+":8000");

    Navigator.push(context, MaterialPageRoute(builder: (context)=>LoginScreen(title: ''),));

  }
}
