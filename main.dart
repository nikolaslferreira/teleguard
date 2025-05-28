import 'package:flutter/material.dart';
import 'pages/login_page.dart';

void main() {
  runApp(const TeleGuardApp());
}

class TeleGuardApp extends StatelessWidget {
  const TeleGuardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Teleguard',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const LoginPage(),
    );
  }
}
