

import 'package:flutter/material.dart';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:greenpaws/plantcartquantity.dart';
import 'package:greenpaws/user_home.dart';
import 'package:greenpaws/view_shopproducts.dart';


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


class viewsingleplant extends StatefulWidget {
  const viewsingleplant({super.key, required this.title});


  final String title;

  @override
  State<viewsingleplant> createState() => _viewsingleplantState();
}
class _viewsingleplantState extends State<viewsingleplant> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    senddata();
  }




  String id='id';
  String plant_name='';
  String scientific_name='';
  String plant_type='';
  String size='';
  String photo='';
  String price='';
  String details='';





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
                    image: NetworkImage(photo),
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
                                            ' $plant_name',
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
                                      // CircleAvatar(
                                      //   backgroundColor: Colors.blueAccent,
                                      //   child: IconButton(
                                      //       onPressed: () {
                                      //         Navigator.push(context, MaterialPageRoute(builder: (context) => MyEditPage(title: "Edit",),));
                                      //       },
                                      //       icon: Icon(
                                      //         Icons.edit_outlined,
                                      //         color: Colors.white,
                                      //         size: 18,
                                      //       )
                                      //   ),
                                      // )
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
                            title: Text('Name'),
                            subtitle: Text(plant_name),
                            leading: Icon(Icons.mail_outline),
                          ),
                          ListTile(
                            title: Text("Scientific Name"),
                            subtitle: Text(scientific_name),
                            leading: Icon(Icons.phone),
                          ),
                          ListTile(
                            title: Text('Size of the plant'),
                            subtitle: Text(size),
                            leading: Icon(Icons.location_city),
                          ),

                          ListTile(
                            title: Text('Plant-type'),
                            subtitle: Text(plant_type),
                            leading: Icon(Icons.mail_outline),
                          ),

                          ListTile(
                            title: Text('Price'),
                            subtitle: Text(price),
                            leading: Icon(Icons.mail_outline),
                          ),
                          ListTile(
                            title: Text('Details'),
                            subtitle: Text(details),
                            leading: Icon(Icons.mail_outline),
                          ),
                          ListTile(
                            title:  ElevatedButton(
                              child: Text('ADD TO CART'),
                              style: ElevatedButton.styleFrom(
                                primary: Colors.green,
                                textStyle: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 10,
                                    fontStyle: FontStyle.normal),
                              ),
                              onPressed: () {
                                // Navigator.push(context, MaterialPageRoute(builder: (context) =>plantcartquantity(title: '',),));

                              },
                            ),

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

                    Navigator.push(context, MaterialPageRoute(builder: (context) =>viewshopproducts(title: '',),));



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
    String pid= sh.getString('pid').toString();
    String imgurl= sh.getString('imgurl').toString();
    final urls=Uri.parse(url+"/myapp/user_viewsingleplant/");
    try{
      final response=await http.post(urls,body:{
        'lid':lid,
        'pid':pid,
      });
      if (response.statusCode == 200) {
        String status = jsonDecode(response.body)['status'];
        if (status=='ok') {

          setState(() {
            plant_name=jsonDecode(response.body)['plant_name'].toString();
            scientific_name=jsonDecode(response.body)['scientific_name'].toString();
            size=jsonDecode(response.body)['size'].toString();

            plant_type=jsonDecode(response.body)['plant_type'].toString();
            photo=imgurl+jsonDecode(response.body)['photo'].toString();
            price=jsonDecode(response.body)['price'].toString();
            details=jsonDecode(response.body)['details'].toString();
            // photo=sh.getString('img_url').toString()+jsonDecode(response.body)['photo'];
            // district=jsonDecode(response.body)['district'].toString();


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