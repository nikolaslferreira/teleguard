import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'login_form_page.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  Future<void> checkServerStatus(BuildContext context) async {
    const url = 'http://127.0.0.1:5000/';
    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200 || response.statusCode == 404) {
        showSnackBar(context, '✅ Servidor está ONLINE');
      } else {
        showSnackBar(context, '⚠️ Erro: ${response.statusCode}');
      }
    } catch (e) {
      showSnackBar(context, '❌ Servidor está OFFLINE');
    }
  }

  void showSnackBar(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), duration: const Duration(seconds: 3)),
    );
  }

  void goToLoginForm(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const LoginFormPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Teleguard',
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 32),
              ElevatedButton.icon(
                icon: const Icon(Icons.login),
                label: const Text('Login Funcionário'),
                onPressed: () => goToLoginForm(context),
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size.fromHeight(50),
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                icon: const Icon(Icons.cloud),
                label: const Text('Situação do Servidor'),
                onPressed: () => checkServerStatus(context),
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size.fromHeight(50),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
