const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

const connectionString = 'postgresql://postgres:Regina2026%40Roberto@db.sjkgpyalbqqsfndekgtb.supabase.co:5432/postgres';

const client = new Client({
  connectionString,
});

async function runMigration() {
  try {
    await client.connect();
    console.log('✅ Conectado a la base de datos de Supabase.');

    const schemaPath = path.join(__dirname, 'schema.sql');
    const schemaSql = fs.readFileSync(schemaPath, 'utf8');

    console.log('🚀 Ejecutando esquema SQL...');
    await client.query(schemaSql);
    
    console.log('🎉 Migración completada exitosamente. Las tablas han sido creadas.');
  } catch (error) {
    console.error('❌ Error al ejecutar el SQL:', error);
  } finally {
    await client.end();
  }
}

runMigration();
