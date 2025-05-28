import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'admin_dashboard_page.dart';


class LoginFormPage extends StatefulWidget {
  const LoginFormPage({super.key});

  @override
  State<LoginFormPage> createState() => _LoginFormPageState();
}

class _LoginFormPageState extends State<LoginFormPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _rgController = TextEditingController();
  final TextEditingController _senhaController = TextEditingController();

  Future<void> login() async {
    const url = 'http://127.0.0.1:5000/auth/login';

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'RG_FUNC': _rgController.text,
          'SENHA': _senhaController.text,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => AdminDashboardPage(nomeFuncionario: data['NOME_FUNC']),
          ),
        );
      } else {
        final data = jsonDecode(response.body);
        _showMessage('❌ Erro: ${data['mensagem']}');
      }
    } catch (e) {
      _showMessage('❌ Erro de conexão com o servidor.');
    }
  }

  void _showMessage(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login Funcionário')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _rgController,
                decoration: const InputDecoration(labelText: 'RG'),
                validator: (value) =>
                value!.isEmpty ? 'Informe seu RG' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _senhaController,
                decoration: const InputDecoration(labelText: 'Senha'),
                obscureText: true,
                validator: (value) =>
                value!.isEmpty ? 'Informe sua senha' : null,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    login();
                  }
                },
                child: const Text('Entrar'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
