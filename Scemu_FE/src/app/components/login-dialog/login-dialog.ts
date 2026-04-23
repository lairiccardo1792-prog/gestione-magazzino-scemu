import { Component, EventEmitter, Input, Output,ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login-dialog',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './login-dialog.html',
  styleUrls: ['./login-dialog.css'],
  encapsulation: ViewEncapsulation.None
})
export class LoginDialog {
  @Input() show = false;
  @Input() success = false;
  @Input() message = '';

  @Output() closed = new EventEmitter<void>();

  close(): void {
    this.closed.emit();
  }
}