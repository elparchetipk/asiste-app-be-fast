"""SMTP email service implementation."""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

from ...application.interfaces import EmailServiceInterface


class SMTPEmailService(EmailServiceInterface):
    """SMTP implementation of EmailServiceInterface."""
    
    def __init__(self):
        self._smtp_server = os.getenv("SMTP_SERVER", "localhost")
        self._smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self._smtp_username = os.getenv("SMTP_USERNAME", "")
        self._smtp_password = os.getenv("SMTP_PASSWORD", "")
        self._smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self._from_email = os.getenv("FROM_EMAIL", "noreply@sicora.elparcheti.co")
        self._from_name = os.getenv("FROM_NAME", "SICORA - AsisTE App")
        
        self._executor = ThreadPoolExecutor(max_workers=5)
    
    def _send_email_sync(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """Send email synchronously."""
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self._from_name} <{self._from_email}>"
            msg["To"] = to_email
            
            # Add text part if provided
            if text_content:
                text_part = MIMEText(text_content, "plain", "utf-8")
                msg.attach(text_part)
            
            # Add HTML part
            html_part = MIMEText(html_content, "html", "utf-8")
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self._smtp_server, self._smtp_port) as server:
                if self._smtp_use_tls:
                    server.starttls()
                
                if self._smtp_username and self._smtp_password:
                    server.login(self._smtp_username, self._smtp_password)
                
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            # Log error in production
            print(f"Error sending email: {e}")
            return False
    
    async def _send_email_async(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """Send email asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor,
            self._send_email_sync,
            to_email,
            subject,
            html_content,
            text_content
        )
    
    async def send_welcome_email(self, to_email: str, user_name: str, temporary_password: str) -> bool:
        """Send welcome email with temporary password."""
        subject = "Bienvenido a SICORA - AsisTE App"
        
        html_content = f"""
        <html>
        <head></head>
        <body>
            <h2>¡Bienvenido a SICORA - AsisTE App!</h2>
            <p>Hola <strong>{user_name}</strong>,</p>
            
            <p>Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales de acceso:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Email:</strong> {to_email}</p>
                <p><strong>Contraseña temporal:</strong> {temporary_password}</p>
            </div>
            
            <p><strong>⚠️ Importante:</strong> Por seguridad, debes cambiar tu contraseña en el primer inicio de sesión.</p>
            
            <p>Puedes acceder a la aplicación en: <a href="https://sicora.elparcheti.co">https://sicora.elparcheti.co</a></p>
            
            <p>Si tienes alguna pregunta, no dudes en contactar al soporte técnico.</p>
            
            <p>Saludos,<br>
            Equipo SICORA - SENA CGMLTI</p>
        </body>
        </html>
        """
        
        text_content = f"""
        ¡Bienvenido a SICORA - AsisTE App!
        
        Hola {user_name},
        
        Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales de acceso:
        
        Email: {to_email}
        Contraseña temporal: {temporary_password}
        
        ⚠️ Importante: Por seguridad, debes cambiar tu contraseña en el primer inicio de sesión.
        
        Puedes acceder a la aplicación en: https://sicora.elparcheti.co
        
        Si tienes alguna pregunta, no dudes en contactar al soporte técnico.
        
        Saludos,
        Equipo SICORA - SENA CGMLTI
        """
        
        return await self._send_email_async(to_email, subject, html_content, text_content)
    
    async def send_password_reset_email(self, to_email: str, user_name: str, reset_token: str) -> bool:
        """Send password reset email."""
        subject = "Restablecer contraseña - SICORA"
        reset_url = f"https://sicora.elparcheti.co/reset-password?token={reset_token}"
        
        html_content = f"""
        <html>
        <head></head>
        <body>
            <h2>Restablecer contraseña</h2>
            <p>Hola <strong>{user_name}</strong>,</p>
            
            <p>Hemos recibido una solicitud para restablecer tu contraseña en SICORA.</p>
            
            <p>Para restablecer tu contraseña, haz clic en el siguiente enlace:</p>
            
            <p><a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Restablecer Contraseña</a></p>
            
            <p>O copia y pega este enlace en tu navegador: {reset_url}</p>
            
            <p><strong>⚠️ Nota:</strong> Este enlace expirará en 1 hora por seguridad.</p>
            
            <p>Si no solicitaste este restablecimiento, puedes ignorar este email.</p>
            
            <p>Saludos,<br>
            Equipo SICORA - SENA CGMLTI</p>
        </body>
        </html>
        """
        
        return await self._send_email_async(to_email, subject, html_content)
    
    async def send_password_changed_notification(self, to_email: str, user_name: str) -> bool:
        """Send notification that password was changed."""
        subject = "Contraseña actualizada - SICORA"
        
        html_content = f"""
        <html>
        <head></head>
        <body>
            <h2>Contraseña actualizada</h2>
            <p>Hola <strong>{user_name}</strong>,</p>
            
            <p>Te informamos que tu contraseña en SICORA ha sido actualizada exitosamente.</p>
            
            <p><strong>Fecha y hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            
            <p>Si no realizaste este cambio, contacta inmediatamente al soporte técnico.</p>
            
            <p>Saludos,<br>
            Equipo SICORA - SENA CGMLTI</p>
        </body>
        </html>
        """
        
        return await self._send_email_async(to_email, subject, html_content)
    
    async def send_account_activation_email(self, to_email: str, user_name: str, activation_token: str) -> bool:
        """Send account activation email."""
        subject = "Activar cuenta - SICORA"
        activation_url = f"https://sicora.elparcheti.co/activate?token={activation_token}"
        
        html_content = f"""
        <html>
        <head></head>
        <body>
            <h2>Activar tu cuenta</h2>
            <p>Hola <strong>{user_name}</strong>,</p>
            
            <p>Para completar tu registro en SICORA, debes activar tu cuenta.</p>
            
            <p>Haz clic en el siguiente enlace para activar tu cuenta:</p>
            
            <p><a href="{activation_url}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Activar Cuenta</a></p>
            
            <p>O copia y pega este enlace en tu navegador: {activation_url}</p>
            
            <p>Saludos,<br>
            Equipo SICORA - SENA CGMLTI</p>
        </body>
        </html>
        """
        
        return await self._send_email_async(to_email, subject, html_content)
    
    async def send_account_deactivation_notification(self, to_email: str, user_name: str) -> bool:
        """Send notification that account was deactivated."""
        subject = "Cuenta desactivada - SICORA"
        
        html_content = f"""
        <html>
        <head></head>
        <body>
            <h2>Cuenta desactivada</h2>
            <p>Hola <strong>{user_name}</strong>,</p>
            
            <p>Te informamos que tu cuenta en SICORA ha sido desactivada.</p>
            
            <p>Si consideras que esto es un error, contacta al administrador del sistema.</p>
            
            <p>Saludos,<br>
            Equipo SICORA - SENA CGMLTI</p>
        </body>
        </html>
        """
        
        return await self._send_email_async(to_email, subject, html_content)
    
    async def send_custom_email(self, to_email: str, subject: str, template: str, context: Dict[str, Any]) -> bool:
        """Send custom email using template."""
        # Simple template substitution
        html_content = template
        for key, value in context.items():
            html_content = html_content.replace(f"{{{{{key}}}}}", str(value))
        
        return await self._send_email_async(to_email, subject, html_content)
