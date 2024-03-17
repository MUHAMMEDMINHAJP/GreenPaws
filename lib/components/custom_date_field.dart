import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:greenpaws/constants.dart';

class CustomDateField extends StatelessWidget {
  const CustomDateField({
    required this.hintText,
    required this.icon,
    this.obscureText = false,
    required this.keyboardType,
    required this.controller,
    this.validator,
    Key? key,
  }) : super(key: key);

  final String hintText;
  final IconData icon;
  final bool obscureText;
  final TextInputType keyboardType;
  final TextEditingController controller;
  final String? Function(String?)? validator;




  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(left: 20.0, right: 20.0, bottom: 15.0),
      child:
      TextFormField(
        cursorColor: kDarkGreenColor,
        controller: controller,
        obscureText: obscureText,
        keyboardType: keyboardType,
        style: GoogleFonts.poppins(
          color: kDarkGreenColor,
          fontWeight: FontWeight.w600,
          fontSize: 15.0,
        ),
        onTap: () async {
          // Set an initial date
          DateTime initialDate = controller.text.isEmpty
              ? DateTime.now()
              : DateTime.parse(controller.text);

          // Open a date picker with the initial date
          DateTime? pickedDate = await showDatePicker(
            context: context,
            initialDate: initialDate,
            firstDate: DateTime(1900),
            lastDate: DateTime.now(),
          );

          if (pickedDate != null) {
            controller.text = "${pickedDate.toLocal()}".split(' ')[0];
          }
        },
        validator: validator,
        decoration: InputDecoration(
          contentPadding: const EdgeInsets.all(18.0),
          filled: true,
          fillColor: kGinColor,
          prefixIcon: Icon(
            icon,
            size: 24.0,
            color: kDarkGreenColor,
          ),
          hintText: hintText,
          hintStyle: GoogleFonts.poppins(
            color: kDarkGreenColor,
            fontWeight: FontWeight.w600,
            fontSize: 15.0,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10.0),
            borderSide: BorderSide(color: kGinColor),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10.0),
            borderSide: BorderSide(color: kDarkGreenColor),
          ),
        ),
      ),
    );
  }

}

