/**
 * Path Resolver для TypeScript скриптов
 * Определяет правильные пути в зависимости от режима запуска (development/app bundle)
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

export interface PathConfig {
    isAppBundle: boolean;
    projectRoot: string;
    dataDirectory: string;
    logsDirectory: string;
    resultsDirectory: string;
    envFile: string;
}

export class PathResolver {
    private static _instance: PathResolver;
    private _config: PathConfig;

    private constructor() {
        this._config = this.detectPaths();
    }

    public static getInstance(): PathResolver {
        if (!PathResolver._instance) {
            PathResolver._instance = new PathResolver();
        }
        return PathResolver._instance;
    }

    /**
     * Определяет режим запуска и соответствующие пути
     */
    private detectPaths(): PathConfig {
        const isAppBundle = this.isRunningInAppBundle();
        
        if (isAppBundle) {
            // macOS app bundle режим
            const homeDir = os.homedir();
            const appDataDir = path.join(homeDir, '.gosilk_staff');
            
            // Создаем директории если их нет
            this.ensureDirectoryExists(appDataDir);
            this.ensureDirectoryExists(path.join(homeDir, 'Library', 'Logs', 'GoSilk Staff'));
            this.ensureDirectoryExists(path.join(appDataDir, 'results'));
            
            return {
                isAppBundle: true,
                projectRoot: this.findProjectRoot(),
                dataDirectory: appDataDir,
                logsDirectory: path.join(homeDir, 'Library', 'Logs', 'GoSilk Staff'),
                resultsDirectory: path.join(appDataDir, 'results'),
                envFile: path.join(appDataDir, '.env')
            };
        } else {
            // Development режим
            const projectRoot = this.findProjectRoot();
            const dataDir = path.join(projectRoot, 'pyqt_app', 'data');
            const logsDir = path.join(projectRoot, 'pyqt_app', 'logs');
            const resultsDir = path.join(projectRoot, 'results');
            
            // Создаем директории если их нет
            this.ensureDirectoryExists(dataDir);
            this.ensureDirectoryExists(logsDir);
            this.ensureDirectoryExists(resultsDir);
            
            return {
                isAppBundle: false,
                projectRoot: projectRoot,
                dataDirectory: dataDir,
                logsDirectory: logsDir,
                resultsDirectory: resultsDir,
                envFile: path.join(projectRoot, '.env')
            };
        }
    }

    /**
     * Проверяет, запущен ли скрипт из macOS app bundle
     */
    private isRunningInAppBundle(): boolean {
        if (process.platform !== 'darwin') {
            return false;
        }
        
        // Проверяем, находимся ли мы внутри .app bundle
        const executablePath = process.execPath;
        return executablePath.includes('.app/Contents/');
    }

    /**
     * Находит корень проекта (где находится package.json)
     */
    private findProjectRoot(): string {
        let currentDir = __dirname;
        
        // Идем вверх по дереву каталогов до тех пор, пока не найдем package.json
        while (currentDir !== path.dirname(currentDir)) {
            const packageJsonPath = path.join(currentDir, 'package.json');
            if (fs.existsSync(packageJsonPath)) {
                return currentDir;
            }
            currentDir = path.dirname(currentDir);
        }
        
        // Если не нашли, используем текущую директорию
        throw new Error('Не удалось найти корень проекта (package.json)');
    }

    /**
     * Создает директорию если она не существует
     */
    private ensureDirectoryExists(dirPath: string): void {
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
        }
    }

    // Public getters
    public get config(): PathConfig {
        return { ...this._config };
    }

    public get isAppBundle(): boolean {
        return this._config.isAppBundle;
    }

    public get projectRoot(): string {
        return this._config.projectRoot;
    }

    public get dataDirectory(): string {
        return this._config.dataDirectory;
    }

    public get logsDirectory(): string {
        return this._config.logsDirectory;
    }

    public get resultsDirectory(): string {
        return this._config.resultsDirectory;
    }

    public get envFile(): string {
        return this._config.envFile;
    }

    /**
     * Получает путь к файлу конфигурации в data директории
     */
    public getConfigFilePath(filename: string): string {
        return path.join(this.dataDirectory, filename);
    }

    /**
     * Получает путь к файлу результатов в results директории
     */
    public getResultsFilePath(filename: string): string {
        return path.join(this.resultsDirectory, filename);
    }

    /**
     * Получает путь к файлу логов в logs директории
     */
    public getLogFilePath(filename: string): string {
        return path.join(this.logsDirectory, filename);
    }

    /**
     * Читает paths.json и возвращает сохраненные пути
     */
    public async getPathsFromConfig(): Promise<{ excelPath: string; directoryPath: string } | null> {
        try {
            const pathsFile = this.getConfigFilePath('paths.json');
            
            if (!fs.existsSync(pathsFile)) {
                return null;
            }
            
            const data = fs.readFileSync(pathsFile, 'utf-8');
            const pathsData = JSON.parse(data);
            
            return {
                excelPath: pathsData.excel_file_path || '',
                directoryPath: pathsData.directory_path || ''
            };
        } catch (error) {
            console.error('❌ Ошибка при чтении paths.json:', error);
            return null;
        }
    }

    /**
     * Проверяет существование всех необходимых файлов и директорий
     */
    public validatePaths(): { isValid: boolean; errors: string[] } {
        const errors: string[] = [];
        
        // Проверяем существование директорий
        if (!fs.existsSync(this.dataDirectory)) {
            errors.push(`Data directory не существует: ${this.dataDirectory}`);
        }
        
        if (!fs.existsSync(this.logsDirectory)) {
            errors.push(`Logs directory не существует: ${this.logsDirectory}`);
        }
        
        if (!fs.existsSync(this.resultsDirectory)) {
            errors.push(`Results directory не существует: ${this.resultsDirectory}`);
        }
        
        // Проверяем существование .env файла
        if (!fs.existsSync(this.envFile)) {
            errors.push(`Файл .env не найден: ${this.envFile}`);
        }
        
        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Получает диагностическую информацию о путях
     */
    public getDiagnosticInfo(): any {
        const validation = this.validatePaths();
        
        return {
            mode: this.isAppBundle ? 'app_bundle' : 'development',
            platform: process.platform,
            paths: {
                projectRoot: this.projectRoot,
                dataDirectory: this.dataDirectory,
                logsDirectory: this.logsDirectory,
                resultsDirectory: this.resultsDirectory,
                envFile: this.envFile
            },
            validation,
            timestamp: new Date().toISOString()
        };
    }
}

// Экспортируем singleton instance
export const pathResolver = PathResolver.getInstance(); 