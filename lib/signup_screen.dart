import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:greenpaws/components/authentication_button.dart';
import 'package:greenpaws/components/custom_text_field.dart';
import 'package:greenpaws/constants.dart';
import 'package:intl/intl.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;

import 'login_screen.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {


  // Your provided list of distinct items for the dropdown
  final List<String> districts = [
    'Kasargod', 'Kannur', 'Kozhikode', 'Wayanad',
    'Malappuram', 'Thrissur', 'Ernakulam', 'Palakkad',
    'Kottayam', 'Alappuzha', 'Idukki', 'Kollam', 'Pathanamthitta', 'Thiruvananthapuram'
  ];


  static String id = 'SignupScreen';

  String gender = "Male";
  // File? uploadimage;
  TextEditingController nameController= new TextEditingController();
  TextEditingController dobController= new TextEditingController();
  TextEditingController emailController= new TextEditingController();
  TextEditingController phoneController= new TextEditingController();
  TextEditingController placeController= new TextEditingController();
  TextEditingController postController= new TextEditingController();
  TextEditingController pinController= new TextEditingController();
  TextEditingController districtController= new TextEditingController();
  TextEditingController passwordController= new TextEditingController();
  TextEditingController cpController= new TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Material(
      child: Stack(
        children: [
          Scaffold(
            body: SafeArea(
              child: SingleChildScrollView(
                child: Container(
                  constraints: BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height * 0.9,
                  ),
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            Text(
                              'Register',
                              style: GoogleFonts.poppins(
                                fontSize: 32.0,
                                fontWeight: FontWeight.w600,
                                color: kDarkGreenColor,
                              ),
                            ),
                            const SizedBox(height: 10.0),
                            Text(
                              'Create a new account',
                              style: GoogleFonts.poppins(
                                color: kGreyColor,
                                fontSize: 16.0,
                              ),
                            ),
                            const SizedBox(height: 40.0),
                            CustomTextField(
                              controller: nameController,
                              hintText: 'Full Name',
                              icon: Icons.person,
                              keyboardType: TextInputType.name,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please enter your full name';
                                }
                                return null; // Return null if the input is valid
                              },

                            ),
                            CustomTextField(
                              controller: phoneController,
                              hintText: 'Phone Number',
                              icon: Icons.phone_android_outlined,
                              keyboardType: TextInputType.number,

                            ),

                            Container(
                              padding: EdgeInsets.only(left: 8),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text('Gender'),
                                  RadioListTile(value: "Male", groupValue: gender, onChanged: (value) { setState(() {gender="Male";}); },title: Text("Male"),),
                                  RadioListTile(value: "Female", groupValue: gender, onChanged: (value) { setState(() {gender="Female";}); },title: Text("Female"),),
                                  RadioListTile(value: "Other", groupValue: gender, onChanged: (value) { setState(() {gender="Other";}); },title: Text("Other"),),
                                ],
                              ),
                            ),
                            const SizedBox(
                              height: 16,
                            ),
                            Padding(
                              padding: EdgeInsets.all(10),
                              child: Container(
                                padding: const EdgeInsets.all(10),
                                child: TextFormField(
                                  controller: dobController,
                                  decoration: InputDecoration(
                                    border: UnderlineInputBorder(),
                                    focusedBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: BorderSide(
                                          color: Colors.black, width: 2.0),
                                    ),
                                    enabledBorder: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(10),
                                      borderSide: BorderSide(
                                        color: Colors.black,
                                        width: 2.0,
                                      ),
                                    ),
                                    icon: InkWell(
                                      child: Icon(
                                        Icons.calendar_today,
                                        color: Colors.black,
                                      ),
                                      onTap: () async {
                                        DateTime? pickedDate = await showDatePicker(
                                            context: context,
                                            initialDate: DateTime(2008),
                                            //get today's date
                                            firstDate: DateTime(1998),
                                            //DateTime.now() - not to allow to choose before today.
                                            lastDate: DateTime(2008));

                                        if (pickedDate != null) {
                                          print(
                                              pickedDate); //get the picked date in the format => 2022-07-04 00:00:00.000

                                          String formattedDate =
                                          DateFormat('yyyy-MM-dd').format(
                                              pickedDate); // format date in required form here we use yyyy-MM-dd that means time is removed
                                          print(
                                              formattedDate); //formatted date output using intl package =>  2022-07-04
                                          // You can format date as per your need

                                          setState(() {
                                            dobController.text =
                                                formattedDate; //set foratted date to TextField value.
                                          });
                                        } else {
                                          print("Date is not selected");
                                        }
                                      },
                                    ),
                                    labelText: 'DOB',
                                  ),
                                  readOnly: true,
                                ),
                              ),
                            ),

                            CustomTextField(
                              controller: emailController,
                              hintText: 'Email',
                              icon: Icons.mail,
                              keyboardType: TextInputType.name,

                            ),






                            CustomTextField(
                              controller: placeController,
                              hintText: 'Place',
                              icon: Icons.place,
                              keyboardType: TextInputType.name,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please enter your full name';
                                }
                                return null; // Return null if the input is valid
                              },

                            ),
                            CustomTextField(
                              controller: postController,
                              hintText: 'Post',
                              icon: Icons.local_post_office_outlined,
                              keyboardType: TextInputType.name,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please enter your post';
                                }
                                return null; // Return null if the input is valid
                              },

                            ),
                            CustomTextField(
                              controller: pinController,
                              hintText: 'Pin',
                              icon: Icons.pin,
                              keyboardType: TextInputType.number,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please enter your pincode';
                                }
                                return null; // Return null if the input is valid
                              },

                            ),
                            CustomTextField(
                              controller: districtController,
                              hintText: 'District',
                              icon: Icons.location_city,
                              keyboardType: TextInputType.name,
                              validator: (value) {
                                if (value!.isEmpty) {
                                  return 'Please enter your District';
                                }
                                return null; // Return null if the input is valid
                              },

                            ),



                            CustomTextField(
                              controller: passwordController,
                              hintText: 'Password',
                              icon: Icons.lock,
                              keyboardType: TextInputType.name,
                            ),
                            CustomTextField(
                              controller: cpController,
                              hintText: 'Confirm Password',
                              icon: Icons.lock,
                              keyboardType: TextInputType.name,
                            ),
                            const SizedBox(height: 15.0),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  'By signing you agree to our ',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 15.0,
                                    fontWeight: FontWeight.w600,
                                    color: kDarkGreenColor,
                                  ),
                                ),
                                Text(
                                  ' Terms of use',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 15.0,
                                    fontWeight: FontWeight.w600,
                                    color: kGreyColor,
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text(
                                  'and ',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 15.0,
                                    fontWeight: FontWeight.w600,
                                    color: kDarkGreenColor,
                                  ),
                                ),
                                Text(
                                  ' privacy notice',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 15.0,
                                    fontWeight: FontWeight.w600,
                                    color: kGreyColor,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                        Padding(
                          padding: const EdgeInsets.only(left: 20.0, right: 20.0),
                          child: AuthenticationButton(
                            label: 'Sign Up',
                            onPressed: () {



                              senddata();
                              
                            },
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
          Positioned(
            top: 30.0,
            left: 20.0,
            child: CircleAvatar(
              backgroundColor: Colors.grey.shade300,
              radius: 20.0,
              child: IconButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                icon: Icon(
                  Icons.arrow_back_ios_new,
                  color: kDarkGreenColor,
                  size: 24.0,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
  void senddata()async {
    String Name = nameController.text;
    String Phno = phoneController.text;
    String Email = emailController.text;
    String Dob = dobController.text;
    String Place = placeController.text;
    String Post = postController.text;
    String Pin = pinController.text;
    String District = districtController.text;
    String Password = passwordController.text;
    String Cpassword = cpController.text;

    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url').toString();

    final urls = Uri.parse('$url/myapp/signup_user/');
    try {
      final response = await http.post(urls, body: {

        'email': Email,
        'name':Name,
        'ph_no':Phno,
        'place':Place,
        'post':Post,
        'pin':Pin,
        'dob':Dob,
        'district':District,
        'gender':gender,
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
            builder: (context) => LoginScreen(title: "Login"),));
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

}
