import os
import tkinter as tk
import ttkbootstrap as ttkb
from mdi import MDIChild
import sqlite3
import logging
import time
import random

# Allow the SQLite path to be configured via the ``ALBA_DB_PATH`` environment
# variable. Defaults to the new database location when the variable is not set.
DEFAULT_DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database", "alba.db")
)
DB_PATH = os.environ.get("ALBA_DB_PATH", DEFAULT_DB_PATH)

# Configure logging for recnum operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alba_recnum.log'),
        logging.StreamHandler()
    ]
)
recnum_logger = logging.getLogger('alba.recnum')

class BaseWindow(MDIChild):
    """Janela base com utilidades comuns."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.current_recnum = None

    def set_title(self, text):
        """Wrapper to update the title label."""
        super().set_title(text)

    def conectar(self):
        """Retorna uma conexão com o banco de dados."""
        conn = sqlite3.connect(DB_PATH)
        
        def robust_text_factory(data):
            if isinstance(data, bytes):
                try:
                    return data.decode('utf-8')
                except UnicodeDecodeError:
                    return data.decode('latin1')
            return data
            
        conn.text_factory = robust_text_factory
        return conn

    def create_standard_message_panel(self, parent_frame):
        """
        Creates a standardized message panel structure for consistent messaging across all windows.
        
        Args:
            parent_frame: The parent frame where the message panel should be added
            
        Returns:
            tuple: (message_frame, message_label) - The created frame and label components
        """
        # Create message panel frame with consistent styling
        message_frame = ttkb.Frame(parent_frame, relief="sunken", borderwidth=2, padding=5)
        message_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Message frame title with consistent styling
        title_label = ttkb.Label(message_frame, text="Mensagens:", font=("Arial", 8, "bold"))
        title_label.pack(anchor=tk.W)
        
        # Message label with consistent styling and word wrapping
        message_label = ttkb.Label(
            message_frame,
            text="Sistema pronto para uso",
            foreground="blue",
            font=("Arial", 8),
            wraplength=400
        )
        message_label.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        
        return message_frame, message_label

    def ensure_message_panel(self, main_frame):
        """
        Ensures the window has a message panel, creating one if it doesn't exist.
        This method should be called during window initialization.
        
        Args:
            main_frame: The main frame of the window where the message panel should be added
        """
        if not hasattr(self, "message_label") or self.message_label is None:
            try:
                message_frame, message_label = self.create_standard_message_panel(main_frame)
                self.message_label = message_label
                self.message_frame = message_frame
                recnum_logger.debug(f"Message panel created for window: {self.__class__.__name__}")
            except Exception as e:
                recnum_logger.error(f"Failed to create message panel for {self.__class__.__name__}: {str(e)}")
                # Create a minimal fallback message label
                self.message_label = ttkb.Label(main_frame, text="", foreground="blue")
                self.message_label.pack(fill=tk.X, padx=5, pady=2)

    def show_message(self, message, msg_type="info"):
        """
        Enhanced message display with consistent styling and auto-clear functionality.
        
        Args:
            message (str): The message to display
            msg_type (str): Type of message - 'info', 'success', 'warning', 'error'
        """
        if hasattr(self, "message_label") and self.message_label is not None:
            # Enhanced color scheme for different message types
            colors = {
                "info": "blue",
                "success": "green",
                "warning": "orange", 
                "error": "red",
                "danger": "red"  # Alias for error
            }
            
            # Update message label with appropriate styling
            self.message_label.config(
                text=message,
                foreground=colors.get(msg_type, "blue")
            )
            
            # Auto-clear message after 5 seconds for non-error messages
            if msg_type not in ["error", "danger"]:
                # Clear any existing auto-clear timer
                if hasattr(self, "_message_clear_timer"):
                    self.after_cancel(self._message_clear_timer)
                
                # Set new auto-clear timer
                self._message_clear_timer = self.after(5000, lambda: self._clear_message())
            
            recnum_logger.debug(f"Message displayed: [{msg_type}] {message}")
        else:
            # Error handling for missing message panels
            error_msg = f"CRITICAL: Window {self.__class__.__name__} is missing message_label attribute. Message: [{msg_type}] {message}"
            recnum_logger.error(error_msg)
            print(f"ERROR: {error_msg}")  # Console fallback for development
            
            # Attempt to create emergency message panel if we have a parent frame
            try:
                # Try to find a suitable parent frame for emergency message panel
                if hasattr(self, 'winfo_children') and self.winfo_children():
                    # Use the first child frame as parent for emergency message panel
                    parent_frame = self.winfo_children()[0]
                    self.ensure_message_panel(parent_frame)
                    
                    # Retry showing the message
                    if hasattr(self, "message_label") and self.message_label is not None:
                        self.show_message(message, msg_type)
                        return
                        
                # If no suitable parent found, create minimal fallback
                self.message_label = ttkb.Label(self, text="", foreground="blue")
                self.message_label.pack(fill=tk.X, padx=5, pady=2)
                self.show_message(message, msg_type)
                
            except Exception as e:
                recnum_logger.error(f"Failed to create emergency message panel: {e}")
                print(f"FATAL: Cannot display message - {message}")

    def _clear_message(self):
        """Internal method to clear the message and reset to default state."""
        if hasattr(self, "message_label") and self.message_label is not None:
            self.message_label.config(
                text="Sistema pronto para uso",
                foreground="blue"
            )

    def setup_confirmation_pattern(self, action_name, timeout_seconds=3):
        """
        Initialize confirmation pattern for a specific action.
        
        Args:
            action_name (str): Unique name for the action (e.g., 'remove', 'delete')
            timeout_seconds (int): Timeout in seconds before confirmation resets
        """
        if not hasattr(self, '_confirmations'):
            self._confirmations = {}
        
        self._confirmations[action_name] = {
            'pending': False,
            'timeout_seconds': timeout_seconds,
            'timer_id': None
        }
        
        recnum_logger.debug(f"Confirmation pattern setup for action: {action_name}")

    def request_confirmation(self, action_name, message, callback_function, *callback_args, **callback_kwargs):
        """
        Request confirmation for an action using two-step confirmation pattern.
        
        Args:
            action_name (str): Unique name for the action
            message (str): Confirmation message to display
            callback_function: Function to call when confirmed
            *callback_args: Arguments to pass to callback function
            **callback_kwargs: Keyword arguments to pass to callback function
            
        Returns:
            bool: True if action should proceed immediately, False if waiting for confirmation
        """
        # Initialize confirmation pattern if not already setup
        if not hasattr(self, '_confirmations') or action_name not in self._confirmations:
            self.setup_confirmation_pattern(action_name)
        
        confirmation = self._confirmations[action_name]
        
        if not confirmation['pending']:
            # First click - show confirmation message
            self.show_message(message, "warning")
            confirmation['pending'] = True
            
            # Store callback information
            confirmation['callback'] = callback_function
            confirmation['callback_args'] = callback_args
            confirmation['callback_kwargs'] = callback_kwargs
            
            # Set timeout to reset confirmation
            if confirmation['timer_id']:
                self.after_cancel(confirmation['timer_id'])
            
            confirmation['timer_id'] = self.after(
                confirmation['timeout_seconds'] * 1000,
                lambda: self._reset_confirmation(action_name)
            )
            
            recnum_logger.debug(f"Confirmation requested for action: {action_name}")
            return False
        else:
            # Second click within timeout - execute action
            self._reset_confirmation(action_name)
            
            try:
                # Execute the callback function
                callback_function(*callback_args, **callback_kwargs)
                recnum_logger.debug(f"Confirmation action executed: {action_name}")
                return True
            except Exception as e:
                error_msg = f"Erro ao executar ação confirmada '{action_name}': {str(e)}"
                recnum_logger.error(error_msg)
                self.show_message(f"Erro ao executar ação: {str(e)}", "error")
                return False

    def _reset_confirmation(self, action_name):
        """
        Reset confirmation state for a specific action.
        
        Args:
            action_name (str): Name of the action to reset
        """
        if hasattr(self, '_confirmations') and action_name in self._confirmations:
            confirmation = self._confirmations[action_name]
            
            # Cancel any pending timer
            if confirmation['timer_id']:
                self.after_cancel(confirmation['timer_id'])
                confirmation['timer_id'] = None
            
            # Reset confirmation state
            confirmation['pending'] = False
            confirmation['callback'] = None
            confirmation['callback_args'] = None
            confirmation['callback_kwargs'] = None
            
            # Clear warning message if it's still showing
            if hasattr(self, "message_label") and self.message_label is not None:
                current_text = self.message_label.cget("text")
                current_color = self.message_label.cget("foreground")
                
                # Only clear if it's still showing a warning message
                if current_color == "orange":
                    self._clear_message()
            
            recnum_logger.debug(f"Confirmation reset for action: {action_name}")

    def is_confirmation_pending(self, action_name):
        """
        Check if a confirmation is currently pending for an action.
        
        Args:
            action_name (str): Name of the action to check
            
        Returns:
            bool: True if confirmation is pending, False otherwise
        """
        if hasattr(self, '_confirmations') and action_name in self._confirmations:
            return self._confirmations[action_name]['pending']
        return False

    def cancel_all_confirmations(self):
        """Cancel all pending confirmations."""
        if hasattr(self, '_confirmations'):
            for action_name in list(self._confirmations.keys()):
                self._reset_confirmation(action_name)
            recnum_logger.debug("All confirmations cancelled")

    def ir_primeiro(self):
        items = self.tree.get_children()
        if items:
            item = items[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def ir_ultimo(self):
        items = self.tree.get_children()
        if items:
            item = items[-1]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def ir_anterior(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        if idx > 0:
            item = items[idx - 1]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def ir_proximo(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.ir_primeiro()
            return
        items = self.tree.get_children()
        idx = items.index(selecionado[0])
        if idx < len(items) - 1:
            item = items[idx + 1]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
            if hasattr(self, "on_select"):
                self.on_select(None)

    def get_next_recnum(self, table_name, max_retries=3):
        """
        Get the next recnum value for a table with comprehensive error handling and retry logic.
        
        Args:
            table_name (str): Name of the table to get next recnum for
            max_retries (int): Maximum number of retry attempts for concurrent scenarios
            
        Returns:
            int: Next recnum value, or None if operation failed
        """
        if not table_name:
            error_msg = "Nome da tabela não pode estar vazio"
            recnum_logger.error(f"get_next_recnum failed: {error_msg}")
            self.show_message(error_msg, "error")
            return None
            
        # Validate table name to prevent SQL injection
        if not table_name.replace('_', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').isalpha():
            error_msg = f"Nome de tabela inválido: {table_name}"
            recnum_logger.error(f"get_next_recnum failed: {error_msg}")
            self.show_message("Nome de tabela contém caracteres inválidos", "error")
            return None
            
        recnum_logger.info(f"Iniciando obtenção de próximo recnum para tabela: {table_name}")
        
        for attempt in range(max_retries):
            conn = None
            try:
                recnum_logger.debug(f"Tentativa {attempt + 1}/{max_retries} para tabela {table_name}")
                
                conn = self.conectar()
                cursor = conn.cursor()
                
                # Use transaction to ensure consistency
                cursor.execute("BEGIN IMMEDIATE")
                
                # Get next recnum with proper handling
                cursor.execute(f"SELECT COALESCE(MAX(recnum), 0) + 1 FROM {table_name}")
                result = cursor.fetchone()
                
                if result is None or result[0] is None:
                    next_recnum = 1
                    recnum_logger.warning(f"Tabela {table_name} vazia, usando recnum = 1")
                else:
                    next_recnum = result[0]
                    
                # Validate the result
                if not isinstance(next_recnum, int) or next_recnum <= 0:
                    raise ValueError(f"Recnum inválido gerado: {next_recnum}")
                
                cursor.execute("COMMIT")
                conn.close()
                
                recnum_logger.info(f"Próximo recnum obtido com sucesso para {table_name}: {next_recnum}")
                return next_recnum
                
            except sqlite3.OperationalError as e:
                error_msg = f"Erro operacional do banco na tentativa {attempt + 1}: {str(e)}"
                recnum_logger.error(f"get_next_recnum - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                # Check if it's a database lock error that might benefit from retry
                if "database is locked" in str(e).lower() or "busy" in str(e).lower():
                    if attempt < max_retries - 1:
                        # Wait with exponential backoff and jitter
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        recnum_logger.info(f"Banco ocupado, aguardando {wait_time:.2f}s antes da próxima tentativa")
                        time.sleep(wait_time)
                        continue
                
                self.show_message(f"Erro na operação do banco: {str(e)}", "error")
                return None
                
            except sqlite3.IntegrityError as e:
                error_msg = f"Erro de integridade do banco: {str(e)}"
                recnum_logger.error(f"get_next_recnum - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                # Integrity errors usually don't benefit from retry
                self.show_message(f"Erro de integridade: {str(e)}", "error")
                return None
                
            except sqlite3.Error as e:
                error_msg = f"Erro geral do SQLite na tentativa {attempt + 1}: {str(e)}"
                recnum_logger.error(f"get_next_recnum - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    wait_time = 0.5 + random.uniform(0, 0.5)
                    recnum_logger.info(f"Erro SQLite, aguardando {wait_time:.2f}s antes da próxima tentativa")
                    time.sleep(wait_time)
                    continue
                    
                self.show_message(f"Erro ao obter próximo recnum: {str(e)}", "error")
                return None
                
            except ValueError as e:
                error_msg = f"Erro de validação: {str(e)}"
                recnum_logger.error(f"get_next_recnum - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                self.show_message(f"Erro de validação: {str(e)}", "error")
                return None
                
            except Exception as e:
                error_msg = f"Erro inesperado na tentativa {attempt + 1}: {str(e)}"
                recnum_logger.error(f"get_next_recnum - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    wait_time = 1.0 + random.uniform(0, 1)
                    recnum_logger.info(f"Erro inesperado, aguardando {wait_time:.2f}s antes da próxima tentativa")
                    time.sleep(wait_time)
                    continue
                    
                self.show_message(f"Erro inesperado ao obter recnum: {str(e)}", "error")
                return None
        
        # All retries exhausted
        error_msg = f"Falha ao obter recnum para {table_name} após {max_retries} tentativas"
        recnum_logger.error(error_msg)
        self.show_message("Falha ao obter próximo número de registro após múltiplas tentativas", "error")
        return None

    def set_current_recnum(self, recnum):
        """
        Set the current recnum for the window with validation and logging.
        
        Args:
            recnum (int or None): The recnum value to set
            
        Returns:
            bool: True if successful, False if validation failed
        """
        try:
            if recnum is not None:
                if not isinstance(recnum, int):
                    try:
                        recnum = int(recnum)
                        recnum_logger.debug(f"Convertido recnum para int: {recnum}")
                    except (ValueError, TypeError) as e:
                        error_msg = f"Recnum deve ser um número inteiro, recebido: {type(recnum).__name__} = {recnum}"
                        recnum_logger.error(f"set_current_recnum failed: {error_msg}")
                        self.show_message("Recnum deve ser um número inteiro", "error")
                        return False
                
                # Validate recnum value
                if recnum <= 0:
                    error_msg = f"Recnum deve ser positivo, recebido: {recnum}"
                    recnum_logger.error(f"set_current_recnum failed: {error_msg}")
                    self.show_message("Recnum deve ser um número positivo", "error")
                    return False
                    
            old_recnum = self.current_recnum
            self.current_recnum = recnum
            
            recnum_logger.debug(f"Recnum atualizado: {old_recnum} -> {recnum}")
            return True
            
        except Exception as e:
            error_msg = f"Erro inesperado ao definir recnum: {str(e)}"
            recnum_logger.error(f"set_current_recnum - {error_msg}")
            self.show_message("Erro interno ao definir recnum", "error")
            return False

    def get_current_recnum(self):
        """Get the current recnum for the window."""
        return self.current_recnum

    def clear_record_state(self):
        """Clear current record state including recnum and current_id."""
        old_recnum = self.current_recnum
        old_id = getattr(self, 'current_id', None)
        
        self.current_recnum = None
        if hasattr(self, 'current_id'):
            self.current_id = None
            
        recnum_logger.debug(f"Estado do registro limpo: recnum {old_recnum} -> None, id {old_id} -> None")

    def validate_recnum_before_insert(self, table_name, recnum):
        """
        Validate that a recnum is safe to use for INSERT operations.
        
        Args:
            table_name (str): Name of the table to check
            recnum (int): The recnum value to validate
            
        Returns:
            bool: True if recnum is safe to use, False otherwise
        """
        if not table_name or recnum is None:
            return False
            
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            # Check if recnum already exists
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE recnum = ?", (recnum,))
            count = cursor.fetchone()[0]
            
            conn.close()
            
            if count > 0:
                error_msg = f"Recnum {recnum} já existe na tabela {table_name}"
                recnum_logger.warning(f"validate_recnum_before_insert: {error_msg}")
                self.show_message(f"Número de registro {recnum} já está em uso", "warning")
                return False
                
            recnum_logger.debug(f"Recnum {recnum} validado para inserção na tabela {table_name}")
            return True
            
        except sqlite3.Error as e:
            error_msg = f"Erro ao validar recnum {recnum} para tabela {table_name}: {str(e)}"
            recnum_logger.error(f"validate_recnum_before_insert - {error_msg}")
            self.show_message("Erro ao validar número de registro", "error")
            return False
        except Exception as e:
            error_msg = f"Erro inesperado ao validar recnum: {str(e)}"
            recnum_logger.error(f"validate_recnum_before_insert - {error_msg}")
            self.show_message("Erro interno na validação", "error")
            return False

    def execute_insert_with_recnum_handling(self, table_name, insert_query, params, description="registro"):
        """
        Execute an INSERT operation with comprehensive recnum error handling.
        
        Args:
            table_name (str): Name of the table for recnum generation
            insert_query (str): The INSERT SQL query
            params (tuple): Parameters for the query
            description (str): Description of what's being inserted (for error messages)
            
        Returns:
            tuple: (success: bool, recnum: int or None, error_message: str or None)
        """
        recnum_logger.info(f"Executando INSERT com tratamento de recnum para {description} na tabela {table_name}")
        
        max_retries = 3
        for attempt in range(max_retries):
            conn = None
            try:
                # Get next recnum
                next_recnum = self.get_next_recnum(table_name)
                if next_recnum is None:
                    return False, None, "Falha ao obter próximo número de registro"
                
                # Validate recnum before use
                if not self.validate_recnum_before_insert(table_name, next_recnum):
                    if attempt < max_retries - 1:
                        recnum_logger.info(f"Recnum {next_recnum} inválido, tentando novamente...")
                        continue
                    return False, None, "Número de registro não disponível após múltiplas tentativas"
                
                # Execute INSERT with transaction
                conn = self.conectar()
                cursor = conn.cursor()
                
                cursor.execute("BEGIN IMMEDIATE")
                
                # Replace first parameter with recnum if it's expected to be recnum
                if params and len(params) > 0:
                    params_list = list(params)
                    params_list[0] = next_recnum  # Assume first param is recnum
                    params = tuple(params_list)
                
                cursor.execute(insert_query, params)
                cursor.execute("COMMIT")
                conn.close()
                
                recnum_logger.info(f"INSERT executado com sucesso: {description} com recnum {next_recnum}")
                return True, next_recnum, None
                
            except sqlite3.IntegrityError as e:
                error_msg = f"Erro de integridade ao inserir {description}: {str(e)}"
                recnum_logger.error(f"execute_insert_with_recnum_handling - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                # Check if it's a recnum conflict
                if "recnum" in str(e).lower() or "unique" in str(e).lower():
                    if attempt < max_retries - 1:
                        recnum_logger.info(f"Conflito de recnum detectado, tentando novamente...")
                        time.sleep(0.1 + random.uniform(0, 0.1))
                        continue
                
                return False, None, f"Erro de integridade: {str(e)}"
                
            except sqlite3.OperationalError as e:
                error_msg = f"Erro operacional ao inserir {description}: {str(e)}"
                recnum_logger.error(f"execute_insert_with_recnum_handling - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                if "database is locked" in str(e).lower() or "busy" in str(e).lower():
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        recnum_logger.info(f"Banco ocupado, aguardando {wait_time:.2f}s...")
                        time.sleep(wait_time)
                        continue
                
                return False, None, f"Erro operacional: {str(e)}"
                
            except Exception as e:
                error_msg = f"Erro inesperado ao inserir {description}: {str(e)}"
                recnum_logger.error(f"execute_insert_with_recnum_handling - {error_msg}")
                
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    wait_time = 1.0 + random.uniform(0, 1)
                    recnum_logger.info(f"Erro inesperado, aguardando {wait_time:.2f}s...")
                    time.sleep(wait_time)
                    continue
                
                return False, None, f"Erro inesperado: {str(e)}"
        
        # All retries exhausted
        error_msg = f"Falha ao inserir {description} após {max_retries} tentativas"
        recnum_logger.error(error_msg)
        return False, None, "Falha na operação após múltiplas tentativas"

    def log_recnum_operation(self, operation, table_name, recnum=None, success=True, error_msg=None):
        """
        Log recnum operations for debugging and audit purposes.
        
        Args:
            operation (str): Type of operation (INSERT, UPDATE, DELETE, SELECT)
            table_name (str): Name of the table
            recnum (int): The recnum involved (if applicable)
            success (bool): Whether the operation was successful
            error_msg (str): Error message if operation failed
        """
        try:
            status = "SUCCESS" if success else "FAILED"
            recnum_str = f"recnum={recnum}" if recnum is not None else "recnum=None"
            
            log_msg = f"RECNUM_OP: {operation} {table_name} {recnum_str} - {status}"
            
            if success:
                recnum_logger.info(log_msg)
            else:
                log_msg += f" - Error: {error_msg}" if error_msg else ""
                recnum_logger.error(log_msg)
                
        except Exception as e:
            # Don't let logging errors break the application
            recnum_logger.error(f"Erro ao registrar operação de recnum: {str(e)}")
