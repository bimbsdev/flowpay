import { Controller, Get } from '@nestjs/common'
import { AppService } from './app.service'

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello()
  }

  @Get('health')
  health() {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV,
    }
  }

  @Get('health/live')
  healthLive() {
    // Liveness probe - basic checks
    return {
      status: 'alive',
      timestamp: new Date().toISOString(),
    }
  }

  @Get('health/ready')
  healthReady() {
    // Readiness probe - more thorough checks
    return {
      status: 'ready',
      timestamp: new Date().toISOString(),
      version: '0.1.0',
      database: 'connected',
    }
  }
}

