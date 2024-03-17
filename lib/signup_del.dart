import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:image_picker/image_picker.dart ';

import 'package:permission_handler/permission_handler.dart';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';

import 'login.dart';
import 'login_screen.dart';

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
      home: const DelSignup(title: 'Delivery Boy Home Page'),
    );
  }
}

class DelSignup extends StatefulWidget {
  const DelSignup({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<DelSignup> createState() => _DelSignupState();
}

class _DelSignupState extends State<DelSignup> {
  TextEditingController NameController =TextEditingController();
  TextEditingController PhnoController =TextEditingController();
  TextEditingController EmailController =TextEditingController();
  TextEditingController PlaceController =TextEditingController();
  TextEditingController PostController =TextEditingController();
  TextEditingController PinController =TextEditingController();
  TextEditingController DistrictController =TextEditingController();
  TextEditingController PasswordController =TextEditingController();
  TextEditingController CpasswordController =TextEditingController();
  String gender="";


  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(

        backgroundColor: Theme.of(context).colorScheme.inversePrimary,

        title: Text(widget.title),
      ),
      body: SingleChildScrollView(

        child: Column(

          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            if (_selectedImage != null) ...{
              InkWell(
                child:
                Image.file(_selectedImage!, height: 400,),
                radius: 399,
                onTap: _checkPermissionAndChooseImage,
                // borderRadius: BorderRadius.all(Radius.circular(200)),
              ),
            }
            else ...{

              // Image(image: NetworkImage(),height: 100, width: 70,fit: BoxFit.cover,),
              InkWell(
                onTap: _checkPermissionAndChooseImage,
                child:Column(
                  children: [
                    Image(image: NetworkImage('https://cdn.pixabay.com/photo/2017/11/10/05/24/select-2935439_1280.png'),height: 200,width: 200,),
                    Text('Upload your Photo',style: TextStyle(color: Colors.cyan))
                  ],
                ),
              ),
            },

            if (_selectedImage1 != null) ...{
              InkWell(
                child:
                Image.file(_selectedImage1!, height: 400,),
                radius: 399,
                onTap: _checkPermissionAndChooseImage1,
                // borderRadius: BorderRadius.all(Radius.circular(200)),
              ),
            } else ...{
              // Image(image: NetworkImage(),height: 100, width: 70,fit: BoxFit.cover,),
              InkWell(
                onTap: _checkPermissionAndChooseImage1,
                child:Column(
                  children: [
                    Image(image: NetworkImage('https://cdn.pixabay.com/photo/2017/11/10/05/24/select-2935439_1280.png'),height: 200,width: 200,),
                    Text('upload id proof',style: TextStyle(color: Colors.cyan))
                  ],
                ),
              ),
            },




            TextFormField(controller:NameController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Username'),),
            TextFormField(controller:PhnoController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Phone Number'),),
            TextFormField(controller:EmailController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Email'),),
            RadioListTile(value: "Male", groupValue: gender, onChanged: (value) { setState(() {gender="Male";}); },title: Text("Male"),),
            RadioListTile(value: "Female", groupValue: gender, onChanged: (value) { setState(() {gender="Female";}); },title: Text("Female"),),
            RadioListTile(value: "Other", groupValue: gender, onChanged: (value) { setState(() {gender="Other";}); },title: Text("Other"),),
            // TextFormField(decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'gender'),),
            TextFormField(controller:PlaceController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Place'),),
            TextFormField(controller:PostController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Post'),),
            TextFormField(controller:PinController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Pin'),),
            TextFormField(controller:DistrictController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'district'),),
            TextFormField(controller:PasswordController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Password'),),
            TextFormField(controller:CpasswordController,decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20),),labelText: 'Confirm Password'),),

            ElevatedButton(onPressed: (){
              senddata();
            }, child: Text('Register'))
            //
          ],
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: _incrementCounter,
      //   tooltip: 'Increment',
      //   child: const Icon(Icons.add),
      // ), // This trailing comma makes auto-formatting nicer for build methods.
    );  }
  void senddata()async {
    String Name = NameController.text;
    String Phno = PhnoController.text;
    String Email = EmailController.text;
    String Place = PlaceController.text;
    String Post = PostController.text;
    String Pin = PinController.text;
    String District = DistrictController.text;

    String Password = PasswordController.text;
    String Cpassword = CpasswordController.text;

    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();

    final urls = Uri.parse('$url/myapp/signup_del/');
    try {
      final response = await http.post(urls, body: {



        'name':Name,
        'Ph_no':Phno,
        'email':Email,
        'place':Place,
        'post':Post,
        'pin':Pin,
        'district':District,
        'gender':gender,
        'photo':photo,
        'idproof':photo1,
        'password':Password,
        'c_password':Cpassword,


      });
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        // String type = jsonDecode(response.body)['type'];
        if (status == 'ok') {
          // if (type == 'user') {
          //   String lid = jsonDecode(response.body)['lid'];
          // sh.setString("lid", lid);

          Navigator.push(context, MaterialPageRoute(
            builder: (context) => LoginScreen(title: "login"),));
          // }
        } else {
          Fluttertoast.showToast(msg: 'Not Found');
        }
      }
      else {
        Fluttertoast.showToast(msg: 'Network Error');
      }
    }
    catch (e) {
      Fluttertoast.showToast(msg: e.toString());
    }

  }
File? _selectedImage;
String? _encodedImage;
Future<void> _chooseAndUploadImage() async {
  final picker = ImagePicker();
  final pickedImage = await picker.pickImage(source: ImageSource.gallery);

  if (pickedImage != null) {
    setState(() {
      _selectedImage = File(pickedImage.path);
      _encodedImage = base64Encode(_selectedImage!.readAsBytesSync());
      photo = _encodedImage.toString();
    });
  }
}

Future<void> _checkPermissionAndChooseImage() async {
  final PermissionStatus status = await Permission.mediaLibrary.request();
  if (status.isGranted) {
    _chooseAndUploadImage();
  } else {
    showDialog(
      context: context,
      builder: (BuildContext context) => AlertDialog(
        title: const Text('Permission Denied'),
        content: const Text(
          'Please go to app settings and grant permission to choose an image.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}
  File? _selectedImage1;
  String? _encodedImage1;
  Future<void> _chooseAndUploadImage1() async {
    final picker = ImagePicker();
    final pickedImage = await picker.pickImage(source: ImageSource.gallery);

    if (pickedImage != null) {
      setState(() {
        _selectedImage1 = File(pickedImage.path);
        _encodedImage1 = base64Encode(_selectedImage1!.readAsBytesSync());
        photo1 = _encodedImage1.toString();
      });
    }
  }

  Future<void> _checkPermissionAndChooseImage1() async {
    final PermissionStatus status = await Permission.mediaLibrary.request();
    if (status.isGranted) {
      _chooseAndUploadImage1();
    } else {
      showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          title: const Text('Permission Denied'),
          content: const Text(
            'Please go to app settings and grant permission to choose an image.',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
  }

  String photo = '';
  String photo1 = '';




}
